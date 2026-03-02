from .SHARED import CONSISTENCY_ERROR_DESC, CROSS_FILE_NOTE, FOOTER, FORMAT_DESC, NOTE, TASK
from .EXEMPLARS import GOOD_EXAMPLES, COT_EXAMPLES, BAD_EXAMPLES

BASIC_STYLE_ANALYSIS_PROMPT = f"""
{TASK}

Your main focus is to find consistency issues. 

{CONSISTENCY_ERROR_DESC}

{FORMAT_DESC}

{NOTE}

------ BEGIN EXAMPLES --------

{GOOD_EXAMPLES}

{COT_EXAMPLES}

------ END EXAMPLES -----------

------ BEGIN BAD EXAMPLES [ DONT DO THIS ] --------

{BAD_EXAMPLES}

------ END BAD EXAMPLES [ DONT DO THIS ] -----------


{FOOTER}
"""

def basic_style_analysis_prompt_function(overrides: dict[str, str]) -> str:
    ovrd = overrides

    return f"""
    {overrides["TASK"]}

    Your main focus is to find consistency issues. 

    {ovrd["CONSISTENCY_ERROR_DESC"]}

    {ovrd["FORMAT_DESC"]}

    {ovrd["NOTE"]}

    ------ BEGIN EXAMPLES --------

    {ovrd["GOOD_EXAMPLES"]}

    {ovrd["COT_EXAMPLES"]}

    ------ END EXAMPLES -----------

    ------ BEGIN BAD EXAMPLES [ DONT DO THIS ] --------

    {ovrd["BAD_EXAMPLES"]}

    ------ END BAD EXAMPLES [ DONT DO THIS ] -----------

    {ovrd["FOOTER"]}
    """

CROSS_FILE_STYLE_ANALYSIS_PROMPT = f"""
{TASK}

Your main focus is finding consistency errors. 

{CONSISTENCY_ERROR_DESC}

{FORMAT_DESC}

{CROSS_FILE_NOTE}

{NOTE}

------ BEGIN EXAMPLES --------

{GOOD_EXAMPLES}

{COT_EXAMPLES}

------ END EXAMPLES -----------

------ BEGIN BAD EXAMPLES [ DONT DO THIS ] --------

{BAD_EXAMPLES}

------ END BAD EXAMPLES [ DONT DO THIS ] -----------

{FOOTER}
"""

def cross_file_style_analysis_prompt_function(overrides: dict[str, str]) -> str:
    ovrd = overrides
    return f"""
    {ovrd["TASK"]}

    Your main focus is finding consistency errors. 

    {ovrd["CONSISTENCY_ERROR_DESC"]}

    {ovrd["FORMAT_DESC"]}

    {ovrd["CROSS_FILE_NOTE"]}

    {ovrd["NOTE"]}

    ------ BEGIN EXAMPLES --------

    {ovrd["GOOD_EXAMPLES"]}

    {ovrd["COT_EXAMPLES"]}

    ------ END EXAMPLES -----------

    ------ BEGIN BAD EXAMPLES [ DONT DO THIS ] --------

    {ovrd["BAD_EXAMPLES"]}

    ------ END BAD EXAMPLES [ DONT DO THIS ] -----------

    {ovrd["FOOTER"]}
    """
