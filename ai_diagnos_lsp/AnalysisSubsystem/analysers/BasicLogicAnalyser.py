#!/usr/bin/env python3
from __future__ import annotations
from typing import TYPE_CHECKING
from langchain_core.runnables import RunnableLambda
from lsprotocol import types
from pygls.workspace import TextDocument
from pathlib import Path

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.BasicLogicAnalysisPrompt import BasicLogicAnalysisPromptFactory
from ai_diagnos_lsp.utils.analyser.chain_invoker import chain_invoker_function_basic
from ai_diagnos_lsp.utils.analyser.llm_generator import LlmFactoryWithConfig
from ai_diagnos_lsp.utils.json_repair import optional_repair_json
from ai_diagnos_lsp.utils.strip_scratchpad import stript_scratchpad

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

        repairs = RunnableLambda(optional_repair_json)

        strip_think = RunnableLambda(stript_scratchpad)

        output =  GeneralDiagnosticsOutputParserFactory()

        chain = prompt | llm | strip_think | repairs |output
        

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

