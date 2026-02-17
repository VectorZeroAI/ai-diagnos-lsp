#!/usr/bin/env python

from typing import Any, Sequence
from langchain_core.runnables import Runnable, RunnableWithFallbacks

from .BasicGeminiLLM import BasicGeminiLlmFactory
from .BasicOpenrouterLLM import OpenrouterLlmFactory
from .BasicGroqLLM import BasicGroqLLMFactory

def BasicOmniproviderLLMFactory(
        model_openrouter: str,
        model_gemini: str,
        model_groq: str,
        api_key_openrouter: str,
        api_key_gemini: str,
        api_key_groq: str,
        fallback_models_gemini: Sequence[str] | None = None,
        fallback_models_groq: Sequence[str] | None = None,
        ) -> RunnableWithFallbacks[Any, Any]:
    """
    The factory function that retuns the omni provider llm.
    """
    llm = OpenrouterLlmFactory(model_openrouter, api_key_openrouter)
    fallbacks: list[Runnable[Any, Any]] = []
    if fallback_models_gemini is not None:
        fallbacks.append(BasicGeminiLlmFactory(model_gemini, api_key_gemini, fallback_models_gemini))
    else:
        fallbacks.append(BasicGeminiLlmFactory(model_gemini, api_key_gemini))

    if fallback_models_groq is not None:
        fallbacks.append(BasicGroqLLMFactory(model_groq, api_key_groq, fallback_models_groq))
    else:
        fallbacks.append(BasicGroqLLMFactory(model_groq, api_key_groq))

    llm = llm.with_fallbacks(fallbacks)
    return llm
