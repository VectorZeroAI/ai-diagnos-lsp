#!/usr/bin/env python3
from __future__ import annotations
from typing import TYPE_CHECKING, Any
from langchain_core.runnables import Runnable
import os
import logging

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicOmniproviderLLM import BasicOmniproviderLLMFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicGeminiLLM import BasicGeminiLlmFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicGroqLLM import BasicGroqLLMFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicCerebrasLLM import BasicCerebrasLLMFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicOpenrouterLLM import OpenrouterLlmFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicOpenAiLLM import OpenAILlmFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicClaudeLLM import BasicClaudeLLMFactoryFunction
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicHuggingFaceLLM import BasicHuggingFaceLLMFactory


if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import user_config

if os.getenv('AI_DIAGNOS_LOG') is not None:
    LOG = True
else:
    LOG = False # pyright: ignore


def LlmFactoryWithConfig(config: user_config) -> Runnable[dict[Any, Any], Any]:
    """
    The llm generator function. Basically a factory function / util that takes the config in and returns 
    the appropriate llm according to the configuration
    """
    if LOG:
        logging.info("Llm Factory with config started")
    try:

        if config["use"] == 'Omniprovider':
            llm = BasicOmniproviderLLMFactory(
                    model_openrouter=config["model_openrouter"],
                    api_key_openrouter=config["api_key_openrouter"],
                    api_key_gemini=config["api_key_gemini"],
                    api_key_cerebras=config['api_key_cerebras'],
                    api_key_huggingface=config['api_key_huggingface'],
                    model_gemini=config["model_gemini"],
                    fallback_models_gemini=config.get("fallback_models_gemini"),
                    api_key_groq=config["api_key_groq"],
                    model_groq=config["model_groq"],
                    fallback_models_groq=config.get("fallback_models_groq"),
                    model_cerebras=config['model_cerebras'],
                    fallback_models_cerebras=config.get('falback_models_cerebras'),
                    model_huggingface=config['model_huggingface'],
                    model_openai=config['model_openai'],
                    model_claude=config['model_claude'],
                    api_key_claude=config['api_key_claude'],
                    api_key_openai=config['api_key_openai']
                    )

        elif config["use"] == 'gemini':
            llm = BasicGeminiLlmFactory(
                    api_key_gemini=config["api_key_gemini"],
                    model_gemini=config["model_gemini"],
                    fallback_gemini_models=config.get("fallback_models_gemini")
                    )

        elif config["use"] == 'Openrouter':
            llm = OpenrouterLlmFactory(
                    model_openrouter=config["model_openrouter"],
                    api_key_openrouter=config["api_key_openrouter"]
                    )

        elif config['use'] == 'groq':
            llm = BasicGroqLLMFactory(
                    model_groq=config['model_groq'],
                    api_key_groq=config['api_key_groq'],
                    fallback_models_groq=config.get('fallback_models_groq')
                    )
        elif config['use'] == 'cerebras':
            llm = BasicCerebrasLLMFactory(
                    model_cerebras=config['model_cerebras'],
                    api_key_cerebras=config['api_key_cerebras'],
                    fallback_models_cerebras=config.get('fallback_models_cerebras')
                    )
        elif config['use'] == 'OpenAI':
            llm = OpenAILlmFactory(
                    model_openai=config['model_openai'],
                    api_key_openai=config['api_key_openai']
                    )
        elif config['use'] == 'huggingface':
            llm = BasicHuggingFaceLLMFactory(
                    api_key_huggingface=config['api_key_huggingface'],
                    model_huggingface=config['model_huggingface']
                    )

        elif config['use'] == 'Claude':
            llm = BasicClaudeLLMFactoryFunction(
                    api_key_claude=config['api_key_claude'],
                    model_claude=config['model_claude']
                    )

        else:
            if LOG:
                logging.error("llm Factory with config recieved invalid config")
            raise ValueError("Invalid configuration recieved")

        return llm # pyright: ignore

    except KeyError as e:
        if LOG:
            logging.error(f"Key error inside llm generator with config. error: {e}")
        raise RuntimeError(f"Key error inside llm generator. error: {e}") from e
