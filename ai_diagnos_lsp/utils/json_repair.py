#!/usr/bin/env python3

from fix_busted_json import repair_json, can_parse_json # pyright: ignore
# I use pyright in strict mode, and the developer of the library doesnt, so pyright always complains because of missing type hints
from langchain_core.messages import AIMessage

import os
import logging

if os.getenv('AI_DIAGNOS_LOG') is not None:
    LOG = True
else:
    LOG = False # pyright: ignore

def optional_repair_json(input_msg: AIMessage) -> AIMessage:
    """
    Takes AIMessage in, fixes json contents, gives AIMessage out. 
    """
    try:
        if LOG:
            logging.info("json repairs tool started")
            logging.info(f"The content of AIMessage is the following : {input_msg.content}")

        if isinstance(input_msg.content, str): # pyright: ignore
            content = input_msg.content

        else:
            if isinstance(input_msg.content, list):

                if len(input_msg.content) > 0:

                    if isinstance(input_msg.content[0], str):
                        content = "\n".join(input_msg.content)

                    elif isinstance(input_msg.content[0], dict):
                        content = ""
                        for i in input_msg.content:
                            if i.get('type') == "text":
                                if i.get('text') is not None:
                                    content = content + i.get('text')
                                else:
                                    continue
                    else:
                        return input_msg
                else:
                    return input_msg
            else:
                return input_msg
        
        assert content is str
        if can_parse_json(content):
            return input_msg
        else:
            if content.startswith('`'):
                content.strip('`')
            if content.startswith('json'):
                content = content[4:]
            try:
                repaired_content: str = repair_json(content)
                if isinstance(repaired_content, str):
                    return AIMessage(content=repaired_content)
                else:
                    return input_msg
            except Exception as e:
                if LOG:
                    logging.error(f"the repair json function call encoutered the following expection {e}. Trying to remove the prefixing backtricks if some are found. ")
                    
    except Exception as e:
        if LOG:
            logging.error(f"json repairs tool encoutered the following error: {e}")
        return input_msg
        

