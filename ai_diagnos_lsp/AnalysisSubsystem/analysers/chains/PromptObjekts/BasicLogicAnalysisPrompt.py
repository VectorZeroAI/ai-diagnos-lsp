#!/usr/bin/env python

from langchain_core.prompts import ChatPromptTemplate

from .prompts.general_logic_analysis_system_prompt import GENERAL_LOGIC_ANALYSIS_SYSTEM_PROMPT

def BasicLogicAnalysisPromptFactory() -> ChatPromptTemplate:
    """
    This is the Prompt Objekt factory for the chain.
    I cant make it just an importable class, because if I do, 
    I would still have to make an instanse of it for it to actually read the prompt. 
    The prompt is stored in a separate file, at the prompts directory. 
    """

    

    LogicAnalysisPrompt = ChatPromptTemplate.from_messages([
        ("system", f"{GENERAL_LOGIC_ANALYSIS_SYSTEM_PROMPT}"),
        ("human", "\n{{{file_content}}}\n\n"),
        ], template_format="mustache")
    return LogicAnalysisPrompt
