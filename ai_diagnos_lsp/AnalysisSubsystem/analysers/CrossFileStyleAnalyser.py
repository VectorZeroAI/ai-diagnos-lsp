#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from langchain_core.runnables import RunnableLambda
from lsprotocol import types
from pygls.workspace import TextDocument

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import (
    GeneralDiagnosticsOutputParserFactory,
)
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.CrossFileStylePrompt import (
    CrossFileStyleAnalysisPromptFactory,
)
from ai_diagnos_lsp.utils.analyser.chain_invoker import chain_invoker_function_cross_file
from ai_diagnos_lsp.utils.analyser.llm_generator import LlmFactoryWithConfig
from ai_diagnos_lsp.utils.json_repair import optional_repair_json
from ai_diagnos_lsp.utils.strip_scratchpad import strip_scratchpad

if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

def CrossFileStyleAnalyserWorker(document: TextDocument | Path, ls: AIDiagnosLSP):
    """
    The Style Analyser worker thread
    """

    try:

        llm = LlmFactoryWithConfig(ls.config)
        
        if isinstance(document, TextDocument):
            filetype = Path(document.path).suffix
        else:
            filetype = document.suffix
        
        prompt = CrossFileStyleAnalysisPromptFactory(ls.config, filetype)

        repairs = RunnableLambda(optional_repair_json)

        strip_think = RunnableLambda(strip_scratchpad)

        output =  GeneralDiagnosticsOutputParserFactory()

        chain = prompt | llm | strip_think | repairs | output
        

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

