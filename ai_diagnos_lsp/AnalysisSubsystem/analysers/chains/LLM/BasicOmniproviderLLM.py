#!/usr/bin/env python

from typing import Any, Sequence
from langchain_core.runnables import Runnable, RunnableWithFallbacks

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicCerebrasLLM import BasicCerebrasLLMFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicClaudeLLM import BasicClaudeLLMFactoryFunction
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicHuggingFaceLLM import BasicHuggingFaceLLMFactory
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.LLM.BasicOpenAiLLM import OpenAILlmFactory

from .BasicGeminiLLM import BasicGeminiLlmFactory
from .BasicOpenrouterLLM import OpenrouterLlmFactory
from .BasicGroqLLM import BasicGroqLLMFactory

def BasicOmniproviderLLMFactory(
        model_openrouter: str,
        model_gemini: str,
        model_groq: str,
        model_cerebras: str,
        model_huggingface: str,
        model_openai: str,
        model_claude: str,
        api_key_openrouter: str,
        api_key_gemini: str,
        api_key_groq: str,
        api_key_cerebras: str,
        api_key_huggingface: str,
        api_key_openai: str,
        api_key_claude: str,
        fallback_models_gemini: Sequence[str] | None = None,
        fallback_models_groq: Sequence[str] | None = None,
        fallback_models_cerebras: Sequence[str] | None = None,
        ) -> RunnableWithFallbacks[Any, Any]:
    """
    The factory function that retuns the omni provider llm.
    """
    llm = OpenrouterLlmFactory(model_openrouter, api_key_openrouter)

    fallbacks: list[Runnable[Any, Any]] = []
    if api_key_gemini != "":
        if fallback_models_gemini is not None:
            fallbacks.append(BasicGeminiLlmFactory(model_gemini, api_key_gemini, fallback_models_gemini))
        else:
            fallbacks.append(BasicGeminiLlmFactory(model_gemini, api_key_gemini))
    if api_key_groq != "":
        if fallback_models_groq:
            fallbacks.append(BasicGroqLLMFactory(model_groq, api_key_groq, fallback_models_groq))
        else:
            fallbacks.append(BasicGroqLLMFactory(model_groq, api_key_groq))
    if api_key_cerebras != "":
        if fallback_models_cerebras is not None:
            fallbacks.append(BasicCerebrasLLMFactory(model_cerebras, api_key_cerebras, fallback_models_cerebras))
        else:
            fallbacks.append(BasicCerebrasLLMFactory(model_cerebras, api_key_cerebras))
        
    if api_key_huggingface != "":
        fallbacks.append(BasicHuggingFaceLLMFactory(api_key_huggingface, model_huggingface))
    
    if api_key_claude != "":
        fallbacks.append(BasicClaudeLLMFactoryFunction(api_key_claude, model_claude))

    if api_key_openai != "":
        fallbacks.append(OpenAILlmFactory(model_openai, api_key_openai))

    llm = llm.with_fallbacks(fallbacks)
    return llm
