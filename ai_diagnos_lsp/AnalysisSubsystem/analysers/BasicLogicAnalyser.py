#!/usr/bin/env python3
from __future__ import annotations
from typing import TYPE_CHECKING
from lsprotocol import types
from pygls.workspace import TextDocument
from pathlib import Path

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.BasicLogicAnalysisPrompt import BasicLogicAnalysisPromptFactory
from ai_diagnos_lsp.utils.analyser.chain_invoker import chain_invoker_function_basic, chain_invoker_function_cross_file
from ai_diagnos_lsp.utils.analyser.llm_generator import LlmFactoryWithConfig

if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

def BasicLogicAnalyserWorker(document: TextDocument | Path, ls: AIDiagnosLSP):
    """
    The Analyser and diagnostics provider thread . 
    TODO : ADD LOGGING
    """

    try:

        llm = LlmFactoryWithConfig(ls.config)
        
        prompt = BasicLogicAnalysisPromptFactory()

        output =  GeneralDiagnosticsOutputParserFactory()

        chain = prompt | llm | output
        

        chain_invoker_function_basic(
                document=document,
                config=ls.config,
                chain=chain,
                ls = ls,
                analysis_type='BasicLogic'
                )

    
    except Exception as e:
        ls.window_show_message(types.ShowMessageParams(types.MessageType(1), f"The whole worker thread errored out with the following error: {e}"))
        return

