#!/usr/bin/env python3

from langchain_anthropic import ChatAnthropic

def BasicClaudeLLMFactoryFunction(
        api_key_claude: str,
        model_claude: str
        ) -> ChatAnthropic
    return ChatAnthropic(api_key=api_key_claude, model=model_claude)
