#!/usr/bin/env python3

from json_repair import repair_json  # pyright: ignore
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser

import os
import logging
import json


"""
NOTE: I basically told pyright to ignore any errors in this file, because the library I use, the fix_busted_json library,
did not add any typehints to their code, so pyright marks it as partially unknown. 
That is just stupid. 
"""

if os.getenv('AI_DIAGNOS_LOG') is not None:
    # its not misspelled. I just call it that way. Why not ? Im the autor, I can name it whatever the hell I want
    LOG = True
else:
    LOG = False # pyright: ignore
    # pyright does flag this line for no reason. 


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

        parser = StrOutputParser()
        content = parser.invoke(input_msg)
        
        assert isinstance(content, str)
        if is_valid_json(content):
            if LOG:
                logging.info(f"json repairs tool passed the input message through because it is valid. input message {content}")
            return input_msg
        else:
            if content.startswith('```json') and content.endswith('```'):
                content = content.removeprefix('```json')
                content = content.removesuffix('```')
                if LOG:
                    logging.info("json repairs tool detected and removed prefixes of markdown format ```")
                # If content is enclosed in markdown codeblock, remove the codeblock. 
                # Newlines dont make json invalid, do they ? I dont think so. If they do, why dont I just strip all of them and thats it ? 
            elif content.startswith('~~~json') and content.endswith('~~~'):
                content = content.removeprefix('~~~json')
                content = content.removesuffix('~~~')
                # Also handle this kind of codeblocks
                if LOG:
                    logging.info("json repairs tool detected and removed prefixes of markdown format ~~~")

            try:
                repaired_content = repair_json(content) # pyright: ignore
                if LOG:
                    logging.info(f"content repairs were done by the repair json of repair json library. Returning the repaired content {content}")
                return AIMessage(content=repaired_content) # pyright: ignore
            except Exception as e:
                if LOG:
                    logging.error(f"the repair json function call encoutered the following exception {e}. Trying to remove the prefixing backtricks if some are found. ")
                return input_msg
                    
    except Exception as e:
        if LOG:
            logging.error(f"json repairs tool encountered the following error: {e}")
        return input_msg
        

