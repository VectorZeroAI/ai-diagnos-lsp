#!/usr/bin/env python

from langchain_core.prompts import ChatPromptTemplate

from .prompts.style_analysis_prompts import CROSS_FILE_STYLE_ANALYSIS_PROMPT

def CrossFileStyleAnalysisPromptFactory():

    return ChatPromptTemplate.from_messages([
        ("system", f"{CROSS_FILE_STYLE_ANALYSIS_PROMPT}"),
        ("human", """
         ---- BEGIN PRIMARY FILE ----
         {{{file_content}}}
         ---- END PRIMARY FILE ----


         ---- BEGIN REFERENCE ONLY CONTEXT ----
         {{{context}}}
         ---- END REFERENCE ONLY CONTEXT
         """),
        ], template_format="mustache")
