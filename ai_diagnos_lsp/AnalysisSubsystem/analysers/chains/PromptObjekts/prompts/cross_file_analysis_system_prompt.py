from .SHARED import CONSISTENCY_ERROR_DESC, CROSS_FILE_NOTE, FOOTER, FORMAT_DESC, LOGIC_ERRORS_DESC, TASK
from .EXEMPLARS import BAD_EXAMPLES, COT_EXAMPLES, GOOD_EXAMPLES

CROSS_FILE_ANALYSIS_SYSTEM_PROMPT = f"""
{TASK}

Your primary focus is to identify LOGIC ERRORS and CONSISTENCY ISSUES in the provided code.
Secondary focus: syntax errors, naming issues, and other code quality problems.

Issue priority categories:
- Logic errors [Error]
- Consistency errors (type mismatches, contradictory state) [Error or Warn]
- Syntax and semantic errors [Error]
- Any other issues you find [Whatever you find appropriate]

{LOGIC_ERRORS_DESC}

{CONSISTENCY_ERROR_DESC}

{FORMAT_DESC}

{CROSS_FILE_NOTE}

------ BEGIN EXAMPLES --------

{GOOD_EXAMPLES}

{COT_EXAMPLES}

------ END EXAMPLES -----------

------ BEGIN BAD EXAMPLES [ DONT DO THIS ] --------

{BAD_EXAMPLES}

------ END BAD EXAMPLES [ DONT DO THIS ] -----------

{FOOTER}
"""

def cross_file_analysis_system_prompt_function(overrides: dict[str, str]) -> str:
    ovrd = overrides
    return f"""
    {ovrd["TASK"]}

    Your primary focus is to identify LOGIC ERRORS and CONSISTENCY ISSUES in the provided code.
    Secondary focus: syntax errors, naming issues, and other code quality problems.

    Issue priority categories:
    - Logic errors [Error]
    - Consistency errors (type mismatches, contradictory state) [Error or Warn]
    - Syntax and semantic errors [Error]
    - Any other issues you find [Whatever you find appropriate]

    {ovrd["LOGIC_ERRORS_DESC"]}

    {ovrd["CONSISTENCY_ERROR_DESC"]}

    {ovrd["FORMAT_DESC"]}

    {ovrd["CROSS_FILE_NOTE"]}

    ------ BEGIN EXAMPLES --------
    {ovrd["GOOD_EXAMPLES"]}

    {ovrd["COT_EXAMPLES"]}
    ------ END EXAMPLES -----------
    ------ BEGIN BAD EXAMPLES [ DONT DO THIS ] --------
    {ovrd["BAD_EXAMPLES"]}
    ------ END BAD EXAMPLES [ DONT DO THIS ] -----------
    {ovrd["FOOTER"]}
    """
