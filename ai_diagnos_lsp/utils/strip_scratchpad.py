from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
import re

def stript_scratchpad(input_msg: AIMessage) -> AIMessage:
    to_string = StrOutputParser()
    content = to_string.invoke(input_msg)
    pattern = r"<think>.*?</think>"

    if content.startswith(r'<think>'):
        content = re.sub(pattern, '', content, re.DOTALL)
        return AIMessage(content)
    else:
        return input_msg

