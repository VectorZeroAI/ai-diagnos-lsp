
#!/usr/bin/env python
"""
The cross file analysis worker thread
"""
from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

import threading
from pathlib import Path
import os
import logging
import time

from pygls.workspace import TextDocument

from lsprotocol import types

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory

from .chains.LLM.BasicOmniproviderLLM import BasicOmniproviderLLMFactory
from .chains.LLM.BasicGeminiLLM import BasicGeminiLlmFactory
from .chains.LLM.BasicGroqLLM import BasicGroqLLMFactory
from .chains.LLM.BasicOpenrouterLLM import OpenrouterLlmFactory
from .chains.PromptObjekts.CrossFileLogicAnalysisPrompt import CrossFileLogicAnalysisPromptFactory

from ai_diagnos_lsp.utils.parser import get_cross_file_context


if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

if os.getenv("AI_DIAGNOS_LOG") is not None:
    LOG = True
else:
    LOG = False # # pyright: ignore

class CrossFileAnalysisConfig(TypedDict):
    scope: list[str]
    max_analysis_depth: int | None
    max_string_size_char: int | None


def CrossFileLogicAnalyser(ls: AIDiagnosLSP, file: TextDocument | Path):
    """
    The worker thread

    Architecture:
        1. build the chain out of prompt + LLM + parser (according to LSP configuration)
        2. Invoke it in a thread with timeout as well as an optional pinger thread that notifies that 
            its still running
        3. register the results to the Diagnostics handling subsystem 
        4. Notify diagnostics handling subsystem to reload diagnostics for the file. 

    """
    
    try:

        if LOG:
            logging.info("Cross File analyser Worker thread started")
        try:
            if ls.config["use_omniprovider"]:

                llm = BasicOmniproviderLLMFactory(
                        model_openrouter=ls.config["model_openrouter"],
                        api_key_openrouter=ls.config["api_key_openrouter"],
                        api_key_gemini=ls.config["api_key_gemini"],
                        model_gemini=ls.config["model_gemini"],
                        fallback_models_gemini=ls.config.get("fallback_models_gemini"),
                        api_key_groq=ls.config["api_key_groq"],
                        model_groq=ls.config["model_groq"],
                        fallback_models_groq=ls.config.get("fallback_models_groq")
                        )

            elif ls.config["use_gemini"]:

                llm = BasicGeminiLlmFactory(
                        api_key_gemini=ls.config["api_key_gemini"],
                        model_gemini=ls.config["model_gemini"],
                        fallback_gemini_models=ls.config.get("fallback_models_gemini")
                        )

            elif ls.config["use_openrouter"]:
                llm = OpenrouterLlmFactory(
                        model_openrouter=ls.config["model_openrouter"],
                        api_key_openrouter=ls.config["api_key_openrouter"]
                        )

            elif ls.config['use_groq']:
                llm = BasicGroqLLMFactory(
                        model_groq=ls.config['model_groq'],
                        api_key_groq=ls.config['api_key_groq'],
                        fallback_models_groq=ls.config['fallback_models_groq']
                        )
            else:
                ls.window_show_message(types.ShowMessageParams(types.MessageType(1), "INVALID CONFIGURATION RECIEVED. One of use parameters must be true !"))
                raise RuntimeError("INVALID CONFIGURATION RECEIVED. One of use parameters must be true !")

            config = ls.config['CrossFileAnalysis']

        except KeyError as e:
            raise RuntimeError(f"lines 49-86, Cross file analyser thread, Key error {e}") from e

        prompt = CrossFileLogicAnalysisPromptFactory()

        output_parser = GeneralDiagnosticsOutputParserFactory()

        chain = prompt | llm | output_parser

        
        if LOG:
            logging.info("chain initialized")


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
                                scope=config['scope'],
                                analysis_max_depth=config.get('max_analysis_depth'),
                                max_string_size_char=config.get('max_string_size_char'),
                                plugins=ls.config.get("plugins")
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
                    raise RuntimeError(f"Key error in Langchain Invoking thread, inside Cross file analyser. On lines 120 - 150 . {e}"
                                       ) from e

                langchain_completed_event.set()
            except Exception as e:
                ls.window_show_message(types.ShowMessageParams(types.MessageType(1), f"Langchain invoking thread errored out with the following error : {e}"))
                langchain_completed_event.set()
                langchain_failed.set()

        threading.Thread(target=LangchainInvokingThread, args=(file,), daemon=True).start()

        if LOG:
            logging.info("starting the cross file analysis chain")
            if isinstance(file, TextDocument):
                logging.info(f"cross file chain started with input file as {file.source}")
                logging.info("cross file chain started with cross file content.")
            else:
                logging.info(f"cross file chain started with input file as {file.read_text()}")
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
            raise RuntimeError(f"Lines 193-196, Cross file analyser thread, Key error {e}") from e

        try:
            timeout = ls.config['timeout']
        except KeyError as e:
            raise RuntimeError(f"Line 2001, Cross file analyser thread, key error {e}") from e

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
            if isinstance(file, TextDocument):
                ls.DiagnosticsHandlingSubsystem.save_new_diagnostic(diagnostics=tmp,
                                                                        document_uri=file.uri,
                                                                        analysis_type='CrossFile'
                                                                    )
                ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(file.uri)
            else:
                ls.DiagnosticsHandlingSubsystem.save_new_diagnostic(diagnostics=tmp,
                                                                        document_uri=file.as_uri(),
                                                                        analysis_type='CrossFile'
                                                                    )
                ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(file.as_uri())
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
    except (KeyError, RuntimeError, Exception) as e:
        if isinstance(e, KeyError):
            raise RuntimeError(f"Unexpected key error in Cross file analyser thread. {e}") from e
        elif isinstance(e, RuntimeError):
            raise RuntimeError(f"Cross file analyser: possibly expected runtime-error {e}") from e
        else:
            raise RuntimeError(f"Unexpectec arbitrary exception occured in Cross file analyser thread. {e}") from e

