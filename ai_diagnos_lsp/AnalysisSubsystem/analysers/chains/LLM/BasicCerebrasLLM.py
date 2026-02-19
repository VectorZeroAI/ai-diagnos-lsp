#!/usr/bin/env python3

from typing import Any
from langchain_core.runnables import Runnable
from pydantic import SecretStr
from langchain_cerebras import ChatCerebras

def BasicCerebrasLLMFactory(model_cerebras: str,  api_key_cerebras: str, fallback_models_cerebras: Sequence[str] | None = None) -> ChatCerebras | RunnableWithFallbacks[Any, Any]:
    """
    This is the Langchain llm objekt Factory function for the Cerebras provider.
    It can produce both an llm for only one model, or an llm for many models . 
    """
    llm: Runnable[dict[Any, Any], Any] = ChatCerebras(
            model=model_cerebras,
            api_key=SecretStr(api_key_cerebras),
            max_retries=0,
            )
    if fallback_models_cerebras is not None:
        fallback_llms: list[Runnable[dict[Any, Any], Any]] = []
        for i in fallback_models_cerebras:
            fallback_llms.append(
                    ChatCerebras(
                        api_key=SecretStr(api_key_cerebras),
                        model=i,
                        max_retries=0
                    )
                )
        llm = llm.with_fallbacks(fallback_llms)
    else:
        pass
    return llm
