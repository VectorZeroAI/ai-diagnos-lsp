#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING
from langchain_core.prompts import ChatPromptTemplate

from ai_diagnos_lsp.utils.get_overrides import get_overrides

from .prompts.general_logic_analysis_system_prompt import cross_file_logic_analysis_prompt_function

if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import user_config

def CrossFileLogicAnalysisPromptFactory(config: user_config, filetype: str):

    ovrd = get_overrides(config, filetype)
    return ChatPromptTemplate.from_messages([
        ("system", f"{cross_file_logic_analysis_prompt_function(ovrd)}"),
        ("human", """
         ---- BEGIN PRIMARY FILE ----
         {{{file_content}}}
         ---- END PRIMARY FILE ----

         ---- BEGIN REFERENCE ONLY CONTEXT ----
         {{{context}}}
         ---- END REFERENCE ONLY CONTEXT ----
         """),
        ], template_format="mustache")
