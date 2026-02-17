#!/usr/bin/env python

from typing import Any, Sequence

from langchain_core.runnables import RunnableSerializable, RunnableWithFallbacks

from .LLM.BasicOmniproviderLLM import BasicOmniproviderLLMFactory

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.BasicAnalysisPrompt import BasicAnalysisPromptFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory

def BasicChainOmniproviderFactory(api_key_openrouter: str,
                                  api_key_gemini: str,
                                  api_key_groq: str,
                                  model_openrouter: str,
                                  model_gemini: str,
                                  model_groq: str,
                                  fallback_models_gemini: Sequence[str] | None = None,
                                  fallback_models_groq: Sequence[str] | None = None
                                  ) -> RunnableSerializable[Any, Any]: 
    """
    This is Chain Creation function for the Omniprovider option, e.g. for everyone
    It falls back through providers in order of Openrouter -> Gemini -> Groq 
    Why ? IDK . 
    
    So it basically just chains the chains in the fallback options, so that every provider is used. 
    """

    # TODO : ADD logging back in

    llm = BasicOmniproviderLLMFactory(
            model_openrouter=model_openrouter,
            model_groq=model_groq,
            model_gemini=model_gemini,
            api_key_gemini=api_key_gemini,
            api_key_groq=api_key_groq,
            api_key_openrouter=api_key_openrouter,
            fallback_models_gemini=fallback_models_gemini,
            fallback_models_groq=fallback_models_groq
            )

    prompt = BasicAnalysisPromptFactory()
    output_parser = GeneralDiagnosticsOutputParserFactory()

    basic_chain_omniprovider: RunnableWithFallbacks[Any, Any] = prompt | llm | output_parser
    return basic_chain_omniprovider
