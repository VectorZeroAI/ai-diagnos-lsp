#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING
from langchain_core.prompts import ChatPromptTemplate
from ai_diagnos_lsp.utils.get_overrides import get_overrides

from .prompts.cross_file_analysis_system_prompt import CROSS_FILE_ANALYSIS_SYSTEM_PROMPT, cross_file_analysis_system_prompt_function
if TYPE_CHECKING:
    from default_config import user_config


def CrossFileAnalysisPromptFactory(config: user_config | None, filetype: str | None) -> ChatPromptTemplate:
    """
    The factory function for creating the file analysis prompt. Takes in the user config and filetype,
    returns the prompt langchain object
    """
    

    if config is None or filetype is None:
        result = ChatPromptTemplate.from_messages([
                ("system", f"{CROSS_FILE_ANALYSIS_SYSTEM_PROMPT}"),
                ("human", """
                 ---- BEGIN PRIMARY FILE ----
                 {{{file_content}}}
                 ---- END PRIMARY FILE ----

                 ---- BEGIN REFERENCE ONLY CONTEXT ----
                 {{{context}}}
                 ---- END REFERENCE ONLY CONTEXT
                 """),
                ], template_format="mustache")
    else:
        try:
            ovrd = get_overrides(config, filetype)
            prompt_f = cross_file_analysis_system_prompt_function(ovrd)
            result = ChatPromptTemplate.from_messages([
                    ("system", f"{prompt_f}"),
                    ("human", """
                     ---- BEGIN PRIMARY FILE ----
                     {{{file_content}}}
                     ---- END PRIMARY FILE ----

                     ---- BEGIN REFERENCE ONLY CONTEXT ----
                     {{{context}}}
                     ---- END REFERENCE ONLY CONTEXT
                     """),
                    ], template_format="mustache")

        except ModuleNotFoundError:
            result = ChatPromptTemplate.from_messages([
                    ("system", f"{CROSS_FILE_ANALYSIS_SYSTEM_PROMPT}"),
                    ("human", """
                     ---- BEGIN PRIMARY FILE ----
                     {{{file_content}}}
                     ---- END PRIMARY FILE ----

                     ---- BEGIN REFERENCE ONLY CONTEXT ----
                     {{{context}}}
                     ---- END REFERENCE ONLY CONTEXT
                     """),
                    ], template_format="mustache")


    return result
