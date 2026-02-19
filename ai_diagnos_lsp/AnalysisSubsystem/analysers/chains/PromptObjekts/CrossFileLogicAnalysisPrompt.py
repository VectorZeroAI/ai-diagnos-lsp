#!/usr/bin/env python

from langchain_core.prompts import ChatPromptTemplate

from .prompts.general_logic_analysis_system_prompt import CROSS_FILE_LOGIC_ANALYSIS_PROMPT

def CrossFileAnalysisPromptFactory():

    return ChatPromptTemplate.from_messages([
        ("system", f"{CROSS_FILE_LOGIC_ANALYSIS_PROMPT}"),
        ("human", """
         ---- BEGIN PRIMARY FILE ----
         {{{file_content}}}
         ---- END PRIMARY FILE ----


         ---- BEGIN REFERENCE ONLY CONTEXT ----
         {{{context}}}
         ---- END REFERENCE ONLY CONTEXT
         """),
        ], template_format="mustache")
