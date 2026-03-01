from .SHARED import CONSISTENCY_ERROR_DESC, CROSS_FILE_NOTE, FOOTER, FORMAT_DESC, LOGIC_ERRORS_DESC, NOTE, TASK
from .EXEMPLARS import BAD_EXAMPLES, COT_EXAMPLES, GOOD_EXAMPLES

GENERAL_LOGIC_ANALYSIS_SYSTEM_PROMPT = f"""
{TASK}

Issue priority categories:
- Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions)
- Consistency errors (variable naming conflicts, type mismatches, contradictory state)

{LOGIC_ERRORS_DESC}

{CONSISTENCY_ERROR_DESC}

{FORMAT_DESC}

{NOTE}

------ BEGIN GOOD EXAMPLES ----------

{GOOD_EXAMPLES}

{COT_EXAMPLES}

------ END GOOD EXAMPLES -------------

------ BEGIN BAD EXAMPLES [ DONT DO THIS ] ----------

{BAD_EXAMPLES}

------ END BAD EXAMPLES [ DONT DO THIS ] ----------

{FOOTER}

"""

CROSS_FILE_LOGIC_ANALYSIS_PROMPT = f"""
{TASK}

Issue priority categories:
- Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions)
- Consistency errors (variable naming conflicts, type mismatches, contradictory state)

{LOGIC_ERRORS_DESC}

{CONSISTENCY_ERROR_DESC}

{FORMAT_DESC}

{NOTE}

------ BEGIN GOOD EXAMPLES ----------

{GOOD_EXAMPLES}

{COT_EXAMPLES}

------ END GOOD EXAMPLES -------------

------ BEGIN BAD EXAMPLES [ DONT DO THIS ] ----------

{BAD_EXAMPLES}

------ END BAD EXAMPLES [ DONT DO THIS ] ----------

{CROSS_FILE_NOTE}

{FOOTER}
"""

def cross_file_logic_analysis_prompt_function(overrides: dict[str, str]) -> str:

    ovrd = overrides
    return f"""
    {ovrd["TASK"]}

    Issue priority categories:
    - Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions)
    - Consistency errors (variable naming conflicts, type mismatches, contradictory state)

    {ovrd["LOGIC_ERRORS_DESC"]}

    {ovrd["CONSISTENCY_ERROR_DESC"]}

    {ovrd["FORMAT_DESC"]}

    {ovrd["NOTE"]}

    ------ BEGIN GOOD EXAMPLES ----------

    {ovrd["GOOD_EXAMPLES"]}

    {ovrd["COT_EXAMPLES"]}

    ------ END GOOD EXAMPLES -------------

    ------ BEGIN BAD EXAMPLES [ DONT DO THIS ] ----------

    {ovrd["BAD_EXAMPLES"]}

    ------ END BAD EXAMPLES [ DONT DO THIS ] ----------

    {ovrd["CROSS_FILE_NOTE"]}

    {ovrd["FOOTER"]}
    """

def general_logic_analysis_system_prompt_with_overrides(overrides: dict[str, str]) -> str:
    ovrd = overrides

    return f"""
    {ovrd["TASK"]}

    Issue priority categories:
    - Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions)
    - Consistency errors (variable naming conflicts, type mismatches, contradictory state)

    {ovrd["LOGIC_ERRORS_DESC"]}
    {ovrd["CONSISTENCY_ERROR_DESC"]}
    {ovrd["FORMAT_DESC"]}
    {ovrd["NOTE"]}

    ------ BEGIN GOOD EXAMPLES ----------
    {ovrd["GOOD_EXAMPLES"]}

    {ovrd["COT_EXAMPLES"]}
    ------ END GOOD EXAMPLES -------------
    ------ BEGIN BAD EXAMPLES [ DONT DO THIS ] ----------
    {ovrd["BAD_EXAMPLES"]}
    ------ END BAD EXAMPLES [ DONT DO THIS ] ----------
    {ovrd["FOOTER"]}
    """
