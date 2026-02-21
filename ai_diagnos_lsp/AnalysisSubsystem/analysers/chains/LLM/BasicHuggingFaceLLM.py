#!/usr/bin/env python3

from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from pydantic import SecretStr

def BasicHuggingFaceLLMFactory(api_key_huggingface: str, model_huggingface: str):
    rate = InMemoryRateLimiter(requests_per_second=0.3)
    return ChatOpenAI(rate_limiter=rate,
                      base_url="https://api-inference.huggingface.co/v1",
                      model=model_huggingface,
                      api_key=SecretStr(api_key_huggingface)
                      )
