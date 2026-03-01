#!/usr/bin/env python
from __future__ import annotations
from typing import TYPE_CHECKING

from langchain_core.prompts import ChatPromptTemplate
import importlib

from .prompts.general_analysis_system_prompt import GENERAL_ANALYSIS_SYSTEM_PROMPT, general_analysis_system_prompt_function
from .prompts.EXEMPLARS import COT_EXAMPLES, BAD_EXAMPLES, GOOD_EXAMPLES
from .prompts.SHARED import FOOTER, FORMAT_DESC, LOGIC_ERRORS_DESC, CONSISTENCY_ERROR_DESC, NOTE, TASK

if TYPE_CHECKING: 
    from ai_diagnos_lsp.default_config import user_config

def BasicAnalysisPromptFactory(config: user_config | None, filetype: str | None) -> ChatPromptTemplate:
    """
    This is the Prompt Objekt factory for the chain.
    I cant make it just an importable class, because if I do, 
    I would still have to make an instanse of it for it to actually read the prompt. 
    The prompt is stored in a separate file, at the prompts directory. 
    """
    if config is None or filetype is None:
        GeneralAnalysisPrompt = ChatPromptTemplate.from_messages([
            ("system", f"{GENERAL_ANALYSIS_SYSTEM_PROMPT}"),
            ("human", "\n{{{file_content}}}\n\n"),
            ], template_format="mustache")
    else:
        try:
            overrides = importlib.import_module(config['prompt_overrides'][filetype])

            ovrd = {
                    "TASK": getattr(overrides, "TASK", TASK),
                    "NOTE": getattr(overrides, "NOTE", NOTE),
                    "LOGIC_ERRORS_DESC": getattr(overrides, "LOGIC_ERRORS_DESC", LOGIC_ERRORS_DESC),
                    "CONSISTENCY_ERROR_DESC": getattr(overrides, "CONSISTENCY_ERROR_DESC", CONSISTENCY_ERROR_DESC),
                    "FORMAT_DESC":  getattr(overrides, "FORMAT_DESC", FORMAT_DESC),
                    "GOOD_EXAMPLES": getattr(overrides, "GOOD_EXAMPLES", GOOD_EXAMPLES),
                    "COT_EXAMPLES": getattr(overrides, "COT_EXAMPLES", COT_EXAMPLES),
                    "BAD_EXAMPLES": getattr(overrides, "BAD_EXAMPLES", BAD_EXAMPLES),
                    "FOOTER": getattr(overrides, "FOOTER", FOOTER),
                    }

            GeneralAnalysisPrompt = ChatPromptTemplate.from_messages([
                ("system", f"{general_analysis_system_prompt_function(ovrd)}"),
                ("human", "\n{{{file_content}}}\n\n"),
                ], template_format="mustache")

        except ModuleNotFoundError:

            GeneralAnalysisPrompt = ChatPromptTemplate.from_messages([
                ("system", f"{GENERAL_ANALYSIS_SYSTEM_PROMPT}"),
                ("human", "\n{{{file_content}}}\n\n"),
                ], template_format="mustache")

        return GeneralAnalysisPrompt
