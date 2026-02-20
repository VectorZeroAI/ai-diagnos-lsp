#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from langchain_core.runnables import Runnable, RunnableLambda
from pygls.workspace import TextDocument
from pathlib import Path

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.BasicAnalysisPrompt import BasicAnalysisPromptFactory
from ai_diagnos_lsp.utils.analyser.chain_invoker import chain_invoker_function_basic
from ai_diagnos_lsp.utils.analyser.llm_generator import LlmFactoryWithConfig
from ai_diagnos_lsp.utils.json_repair import optional_repair_json

if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

def BasicDiagnoseFunctionWorker(document: TextDocument | Path, ls: AIDiagnosLSP):
    """
    The Analyser and diagnostics provider thread
    """
    try:

        llm = LlmFactoryWithConfig(ls.config)
        prompt = BasicAnalysisPromptFactory()
        output = GeneralDiagnosticsOutputParserFactory()

        repairs = RunnableLambda(optional_repair_json)

        chain: Runnable[Any, Any] = prompt | llm | repairs | output 

        chain_invoker_function_basic(document, ls.config, chain, ls, 'Basic')

    except Exception as e:
        raise RuntimeError(f"The whole basic analysis Worker thread quit for the following reason : {e}") from e
