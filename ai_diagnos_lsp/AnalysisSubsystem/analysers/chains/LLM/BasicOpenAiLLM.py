#!/usr/bin/env python3

from langchain_openai import ChatOpenAI

from pydantic import SecretStr

def OpenAILlmFactory(model_openai: str, api_key_openai: str) -> ChatOpenAI:
    """
    This is the Langchain llm objekt Factory function for the Openrouter provider.
    It can not be created with fallback models due to how openrouter counts ratelimits. 
    They are per key / account, not per model, so it would be utterly uselles. 
    """
    llm = ChatOpenAI(
            model=model_openai,
            api_key=SecretStr(api_key_openai),
            max_retries=0
            )
    return llm
