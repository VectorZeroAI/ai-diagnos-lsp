
#!/usr/bin/env python
"""
The cross file analysis worker thread
"""
from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from pathlib import Path
import os
import logging

from pygls.workspace import TextDocument

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory
from ai_diagnos_lsp.utils.analyser.chain_invoker import chain_invoker_function
from ai_diagnos_lsp.utils.analyser.llm_generator import LlmFactoryWithConfig

from .chains.PromptObjekts.CrossFileLogicAnalysisPrompt import CrossFileLogicAnalysisPromptFactory



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

        prompt = CrossFileLogicAnalysisPromptFactory()

        llm = LlmFactoryWithConfig(ls.config)

        output_parser = GeneralDiagnosticsOutputParserFactory()

        chain = prompt | llm | output_parser

        if LOG:
            logging.info("chain initialized")

        chain_invoker_function(file, ls.config, chain, ls)

    except (KeyError, RuntimeError, Exception) as e:
        if isinstance(e, KeyError):
            raise RuntimeError(f"Unexpected key error in Cross file analyser thread. {e}") from e
        elif isinstance(e, RuntimeError):
            raise RuntimeError(f"Cross file analyser: possibly expected runtime-error {e}") from e
        else:
            raise RuntimeError(f"Unexpectec arbitrary exception occured in Cross file analyser thread. {e}") from e

