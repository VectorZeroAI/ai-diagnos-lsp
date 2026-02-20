#!/usr/bin/env python3

from fix_busted_json import repair_json, can_parse_json # pyright: ignore
# I use pyright in strict mode, and the developer of the library doesnt, so pyright always complains because of missing type hints
from langchain_core.messages import AIMessage

def optional_repair_json(input: AIMessage) -> AIMessage:
    """
    Takes AIMessage in, fixes json contents, gives AIMessage out. 
    """
    if isinstance(input.content, str): # pyright: ignore
        content = input.content
    else:
        content = "\n".join(input.content)
    
    if can_parse_json(content):
        return input
    else:
        repaired_content: str = repair_json(content)
        if isinstance(repaired_content, str):
            return AIMessage(content=repaired_content)
        else:
            return input

