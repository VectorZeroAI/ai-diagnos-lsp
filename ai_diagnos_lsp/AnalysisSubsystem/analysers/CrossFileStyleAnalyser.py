#!/usr/bin/env python3

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from lsprotocol import types
from pygls.workspace import TextDocument
from pathlib import Path
from langchain_core.runnables import Runnable, RunnableLambda

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.CrossFileStylePrompt import CrossFileStyleAnalysisPromptFactory
from ai_diagnos_lsp.utils.analyser.chain_invoker import chain_invoker_function_cross_file
from ai_diagnos_lsp.utils.analyser.llm_generator import LlmFactoryWithConfig
from ai_diagnos_lsp.utils.json_repair import optional_repair_json

if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

def CrossFileStyleAnalyserWorker(document: TextDocument | Path, ls: AIDiagnosLSP):
    """
    The Style Analyser worker thread
    """

    try:

        llm = LlmFactoryWithConfig(ls.config)
        
        prompt = CrossFileStyleAnalysisPromptFactory()

        repairs = RunnableLambda(optional_repair_json)

        output =  GeneralDiagnosticsOutputParserFactory()

        chain: Runnable[dict[Any, Any], Any] = prompt | llm | repairs | output
        

        chain_invoker_function_cross_file(
                document=document,
                config=ls.config,
                chain=chain,
                ls = ls,
                analysis_type='CrossFileStyle'
                )

    
    except Exception as e:
        ls.window_show_message(types.ShowMessageParams(types.MessageType(1), f"The whole Cross File Style Analysis worker thread errored out with the following error: {e}"))
        return

