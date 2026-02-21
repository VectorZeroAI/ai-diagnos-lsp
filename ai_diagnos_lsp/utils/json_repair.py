#!/usr/bin/env python3

from fix_busted_json import json_matching
from json_repair import repair_json  # pyright: ignore
from langchain_core.messages import AIMessage

import os
import logging
import json


"""
NOTE: I basically told pyright to ignore any errors in this file, because the library I use, the fix_busted_json library,
did not add any typehints to their code, so pyright marks it as partially unknown. 
That is just stupid. 
"""

if os.getenv('AI_DIAGNOS_LOG') is not None:
    LOG = True
else:
    LOG = False # pyright: ignore


def is_valid_json(json_in: str) -> bool:
    try:
        json.loads(json_in)
        return True
    except json.JSONDecodeError:
        return False

def optional_repair_json(input_msg: AIMessage) -> AIMessage:
    """
    Takes AIMessage in, fixes json contents, gives AIMessage out. 
    """
    try:
        if LOG:
            logging.info("json repairs tool started")
            logging.info(f"The content of AIMessage is the following : {str(input_msg.content)}") # pyright: ignore

        if isinstance(input_msg.content, str): # pyright: ignore
            content = input_msg.content

        else:
            if isinstance(input_msg.content, list): # pyright: ignore

                if len(input_msg.content) > 0:   # pyright: ignore

                    if isinstance(input_msg.content[0], str): # pyright: ignore
                        content = "\n".join(input_msg.content) # pyright: ignore

                    elif isinstance(input_msg.content[0], dict): # pyright: ignore
                        content = ""
                        for i in input_msg.content:  # pyright: ignore
                            if i.get('type') == "text":  # pyright: ignore
                                if i.get('text') is not None:  # pyright: ignore
                                    content = content + i.get('text')   # pyright: ignore
                                else:
                                    continue
                    else:
                        return input_msg
                else:
                    return input_msg
            else:
                return input_msg
        
        assert isinstance(content, str)
        if is_valid_json(content):
            return input_msg
        else:
            if content.startswith('`'):
                content = content[3:-3]
                # Slice the 3 prefixing and 3 ending backtricks out. 
            if content.startswith('json'):
                content = content[4:]
            try:
                repaired_content = repair_json(content, True) # pyright: ignore
                if isinstance(repaired_content, (dict, list)):
                    return AIMessage(content=repaired_content) # pyright: ignore
                else:
                    return input_msg
            except Exception as e:
                if LOG:
                    logging.error(f"the repair json function call encoutered the following exception {e}. Trying to remove the prefixing backtricks if some are found. ")
                return input_msg
                    
    except Exception as e:
        if LOG:
            logging.error(f"json repairs tool encountered the following error: {e}")
        return input_msg
        

