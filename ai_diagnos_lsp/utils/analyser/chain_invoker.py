#!/usr/bin/env python3

from __future__ import annotations


from typing import TYPE_CHECKING, Any
import threading
from pathlib import Path
import time
import logging
import os

from langchain_core.runnables import Runnable
from pygls.workspace import TextDocument

from lsprotocol import types

from ..parser import get_cross_file_context

if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import user_config
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

if os.getenv('AI_DIAGNOS_LOG') is not None:
    LOG = True
else:
    LOG = False # pyright: ignore


def chain_invoker_function_cross_file(document: TextDocument | Path, config: user_config, chain: Runnable[Any, Any], ls: AIDiagnosLSP) -> None:
    """
    Abstracts away the copy pasta of invoking langchain. 
    The smart thing is passing the chain directly in as a runnable. 
    The idea is that aliasing means pointers, and I can alias my assembled chain to the argument, effectively 
    passing the pointer to the function in. 
    """
    langchain_completed_event = threading.Event()
    langchain_timed_out = threading.Event()
    langchain_failed = threading.Event()

    tmp = None

    def LangchainInvokingThread(document: TextDocument | Path):
        try:
            try:
                nonlocal tmp
                if LOG:
                    logging.info("Langchain invoking thread inside cross file analyser started")
                context = get_cross_file_context(
                            document,
                            scope=config['CrossFileAnalysis']['scope'],
                            analysis_max_depth=config['CrossFileAnalysis'].get('max_analysis_depth'),
                            max_string_size_char=config['CrossFileAnalysis'].get('max_string_size_char'),
                            plugins=config.get("plugins")
                            )

                if isinstance(document, TextDocument):
                    tmp = chain.invoke({
                        "file_content": document.source,
                        "context": context
                    })

                else:
                    tmp = chain.invoke({
                        "file_content": document.read_text(),
                        "context": context
                    })

                if LOG:
                    logging.info(f"""
                                 Cross file analysis langchain started with the following input: 
                                 {document.source if isinstance(document, TextDocument) else document.read_text()}
                                 And context :
                                 {context}
                                 """)
            except KeyError as e:
                raise RuntimeError(f"Key error in Langchain Invoking thread, inside Cross file analyser. On lines 110 - 130 . {e}"
                                   ) from e

            langchain_completed_event.set()
        except Exception as e:
            ls.window_show_message(types.ShowMessageParams(types.MessageType(1), f"Langchain invoking thread errored out with the following error : {e}"))
            langchain_completed_event.set()
            langchain_failed.set()

    threading.Thread(target=LangchainInvokingThread, args=(document,), daemon=True).start()

    if LOG:
        logging.info("starting the cross file analysis chain")
        if isinstance(document, TextDocument):
            logging.info(f"cross file chain started with input file as {document.source}")
            logging.info("cross file chain started with cross file content.")
        else:
            logging.info(f"cross file chain started with input file as {document.read_text()}")
            logging.info("cross file chain started with cross file content.")


    def LangchainStillRunningPingerThread(ls: AIDiagnosLSP, show_progress_every_ms: int):
        if LOG:
            logging.info("Langchain Pinger thread started")

        counter = 1

        while not (langchain_completed_event.is_set() or langchain_timed_out.is_set()):
            ls.window_show_message(types.ShowMessageParams(types.MessageType(3), f"Langchain still running [{counter}]"))
            counter = counter + 1
            time.sleep(show_progress_every_ms / 1000)
            if LOG:
                logging.info("Langchain is still running")

        if LOG:
            logging.info("Langchain Pinger thread exited")
            
    try:
        if ls.config['show_progress']:
            threading.Thread(target=LangchainStillRunningPingerThread, args=(ls, ls.config['show_progress_every_ms']), daemon=True).start()
    except KeyError as e:
        raise RuntimeError(f"Lines 145-146, Cross file analyser thread, Key error {e}") from e

    try:
        timeout = ls.config['timeout']
    except KeyError as e:
        raise RuntimeError(f"Line 151, Cross file analyser thread, key error {e}") from e

    if timeout > threading.TIMEOUT_MAX:
        timeout = threading.TIMEOUT_MAX
        
    if langchain_completed_event.wait(timeout):
        pass
    else:
        langchain_timed_out.set()
        ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Langchain timed out"))
        return

    if langchain_failed.is_set():
        ls.window_show_message(types.ShowMessageParams(types.MessageType(1), "Langchain FAILED"))
        return


    try:
        if isinstance(document, TextDocument):
            ls.DiagnosticsHandlingSubsystem.save_new_diagnostic(diagnostics=tmp,
                                                                    document_uri=document.uri,
                                                                    analysis_type='CrossFile'
                                                                )
            ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(document.uri)
        else:
            ls.DiagnosticsHandlingSubsystem.save_new_diagnostic(diagnostics=tmp,
                                                                    document_uri=document.as_uri(),
                                                                    analysis_type='CrossFile'
                                                                )
            ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(document.as_uri())
        if LOG:
            logging.info("Cross file analyser : Published the diagnostics")

    except Exception as e:
        if LOG:
            logging.error("Cross File Analyser : Couldnt register diagnostics into Diagnostics handling subsystem")
        ls.window_show_message(types.ShowMessageParams(types.MessageType(1), f"Couldnt register diagnostics due to the following reason: {e}"))
        return
    else:
        if LOG:
            logging.info("Cross file analyser : sucsessfully registered the diagnostics into the Diagnostics handling subsystem")
        return
