from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
import json
import re

def find_json_inside_str(string: str) -> str:
    """ Find the json and returns json only, or an empty string if nothings found. """
    depth: int = 0
    end: int = 0

    reversed_string = string[::-1]
    if not reversed_string.startswith(r'}'):
        return ""

    for index, char in enumerate(reversed_string):
        if char == r'{':
            depth = depth - 1
        if char == r'}':
            depth = depth + 1
        if depth == 1:
            end = index
            break

    rev_json = reversed_string[:end+1]
    return rev_json[::-1]

    



def strip_scratchpad(input_msg: AIMessage) -> AIMessage:
    to_string = StrOutputParser()
    content = to_string.invoke(input_msg)
    pattern = r"<think>.*?</think>"

    if content.startswith(r'<think>'):
        if r'</think>' in content:
            content = re.sub(pattern, r'', content, flags=re.DOTALL)
            return AIMessage(content)
        else:
            content_json = find_json_inside_str(content)
            try:
                json.loads(content_json)
            except json.JSONDecodeError:
                return input_msg
            else:
                return AIMessage(content_json)
    else:
        return input_msg

