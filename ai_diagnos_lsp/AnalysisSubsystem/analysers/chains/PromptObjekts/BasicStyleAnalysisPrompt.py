#!/usr/bin/env python
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import user_config

from langchain_core.prompts import ChatPromptTemplate

from .prompts.style_analysis_prompts import basic_style_analysis_prompt_function

from ai_diagnos_lsp.utils.get_overrides import get_overrides

def BasicStyleAnalysisPromptFactory(user_config: user_config, filetype: str) -> ChatPromptTemplate:
    """
    This is the Prompt Objekt factory for the chain.
    I cant make it just an importable class, because if I do, 
    I would still have to make an instanse of it for it to actually read the prompt. 
    The prompt is stored in a separate file, at the prompts directory. 
    """
    ovrd = get_overrides(user_config, filetype)
    
    LogicAnalysisPrompt = ChatPromptTemplate.from_messages([
        ("system", f"{basic_style_analysis_prompt_function(ovrd)}"),
        ("human", "\n{{{file_content}}}\n\n"),
        ], template_format="mustache")
    return LogicAnalysisPrompt
