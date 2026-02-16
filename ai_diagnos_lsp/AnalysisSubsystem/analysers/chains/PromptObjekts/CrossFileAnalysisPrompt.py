#!/usr/bin/env python

from langchain_core.prompts import ChatPromptTemplate

from .prompts.cross_file_analysis_system_prompt import CROSS_FILE_ANALYSIS_SYSTEM_PROMPT

def CrossFileAnalysisPromptFactory():

    return ChatPromptTemplate.from_messages([
        ("system", f"{CROSS_FILE_ANALYSIS_SYSTEM_PROMPT}"),
        ("human", "\n{{file_content}}\n\n"),
        ("human", "\n{{context}}\n\n")
        ], template_format="mustache")
