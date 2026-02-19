#!/usr/bin/env python3
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from langchain_core.runnables import Runnable

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicOmniproviderLLM import BasicOmniproviderLLMFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicGeminiLLM import BasicGeminiLlmFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicGroqLLM import BasicGroqLLMFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicOpenrouterLLM import OpenrouterLlmFactory

if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import user_config

def LlmFactoryWithConfig(config: user_config) -> Runnable[Any, Any]:
    """
    The llm generator function. Basically a factory function / util that takes the config in and returns 
    the appropriate llm according to the configuration
    """
    try:

        if config["use_omniprovider"]:
            llm = BasicOmniproviderLLMFactory(
                    model_openrouter=config["model_openrouter"],
                    api_key_openrouter=config["api_key_openrouter"],
                    api_key_gemini=config["api_key_gemini"],
                    model_gemini=config["model_gemini"],
                    fallback_models_gemini=config.get("fallback_models_gemini"),
                    api_key_groq=config["api_key_groq"],
                    model_groq=config["model_groq"],
                    fallback_models_groq=config.get("fallback_models_groq")
                    )

        elif config["use_gemini"]:
            llm = BasicGeminiLlmFactory(
                    api_key_gemini=config["api_key_gemini"],
                    model_gemini=config["model_gemini"],
                    fallback_gemini_models=config.get("fallback_models_gemini")
                    )

        elif config["use_openrouter"]:
            llm = OpenrouterLlmFactory(
                    model_openrouter=config["model_openrouter"],
                    api_key_openrouter=config["api_key_openrouter"]
                    )

        elif config['use_groq']:
            llm = BasicGroqLLMFactory(
                    model_groq=config['model_groq'],
                    api_key_groq=config['api_key_groq'],
                    fallback_models_groq=config.get('fallback_models_groq')
                    )
        else:
            raise ValueError("Invalid configuration recieved")
        return llm

    except KeyError as e:
        raise RuntimeError(f"Key error inside llm generator. error: {e}") from e
