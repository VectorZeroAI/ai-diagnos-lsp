#!/usr/bin/env python

from langchain_core.prompts import ChatPromptTemplate
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.prompts.general_analysis_prompt import GENERAL_ANALYSIS_PROMPT

def BasicAnalysisPromptFactory() -> ChatPromptTemplate:
    """
    This is the Prompt Objekt factory for the chain.
    I cant make it just an importable class, because if I do, 
    I would still have to make an instanse of it for it to actually read the prompt. 
    The prompt is stored in a separate file, at the prompts directory. 
    """

    

    GeneralAnalysisPrompt = ChatPromptTemplate.from_messages([
            ("system", f"{GENERAL_ANALYSIS_PROMPT}"),
            ("human", "\n{{file_content}}\n\n"),
            ], template_format="mustache")
    return GeneralAnalysisPrompt
