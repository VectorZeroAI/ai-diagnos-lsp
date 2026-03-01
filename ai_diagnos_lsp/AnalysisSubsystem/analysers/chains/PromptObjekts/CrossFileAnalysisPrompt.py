#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING
from langchain_core.prompts import ChatPromptTemplate

from .prompts.cross_file_analysis_system_prompt import CROSS_FILE_ANALYSIS_SYSTEM_PROMPT, cross_file_analysis_system_prompt_function
if TYPE_CHECKING:
    from default_config import user_config


def CrossFileAnalysisPromptFactory(config: user_config | None, filetype: str | None) -> ChatPromptTemplate:
    

    if config is None or filetype is None:
        result = ChatPromptTemplate.from_messages([
                ("system", f"{CROSS_FILE_ANALYSIS_SYSTEM_PROMPT}"),
                ("human", """
                 ---- BEGIN PRIMARY FILE ----
                 {{{file_content}}}
                 ---- END PRIMARY FILE ----

                 ---- BEGIN REFERENCE ONLY CONTEXT ----
                 {{{context}}}
                 ---- END REFERENSE ONLY CONTEXT
                 """),
                ], template_format="mustache")
    else:
        try:
            result = cross_file_analysis_system_prompt_function(ovrd)

        except ModuleNotFoundError:

            GeneralAnalysisPrompt = ChatPromptTemplate.from_messages([
                ("system", f"{GENERAL_ANALYSIS_SYSTEM_PROMPT}"),
                ("human", "\n{{{file_content}}}\n\n"),
                ], template_format="mustache")


    return result
