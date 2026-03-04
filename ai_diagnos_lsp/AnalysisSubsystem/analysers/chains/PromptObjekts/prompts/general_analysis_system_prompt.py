from __future__ import annotations

from .SHARED import FOOTER, FORMAT_DESC, LOGIC_ERRORS_DESC, CONSISTENCY_ERROR_DESC, TASK
from .EXEMPLARS import BAD_EXAMPLES, COT_EXAMPLES, GOOD_EXAMPLES


GENERAL_ANALYSIS_SYSTEM_PROMPT = f"""
{TASK}

Issue priority categories:
- Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions) [Error]
- Consistency errors (type mismatches, contradictory state) [Error or warning]
- Syntax and semantic errors [Error]
- Any other issues you find [Whatever you find appropriate]

{LOGIC_ERRORS_DESC}

{CONSISTENCY_ERROR_DESC}

{FORMAT_DESC}

------ BEGIN EXAMPLES --------

{GOOD_EXAMPLES}

---------

{COT_EXAMPLES}

------- END EXAMPLES ----------

------- BEGIN BAD EXAMPLES [DONT DO THIS] --------

{BAD_EXAMPLES}

------- END BAD EXAMPLES [DONT DO THIS] -----------

{FOOTER}

"""

def general_analysis_system_prompt_function(overrides: dict[str, str]) -> str:
    
    ovrd = overrides

    return f"""
    {ovrd["TASK"]}

    Issue priority categories:
    - Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions) [Error]
    - Consistency errors (type mismatches, contradictory state) [Error or warning]
    - Syntax and semantic errors [Error]
    - Any other issues you find [Whatever you find appropriate]

    {ovrd["LOGIC_ERRORS_DESC"]}

    {ovrd["CONSISTENCY_ERROR_DESC"]}

    {ovrd["FORMAT_DESC"]}

    ------ BEGIN EXAMPLES --------

    {ovrd["GOOD_EXAMPLES"]}

    ---------

    {ovrd["COT_EXAMPLES"]}

    ------- END EXAMPLES ----------

    ------- BEGIN BAD EXAMPLES [DONT DO THIS] --------

    {ovrd["BAD_EXAMPLES"]}

    ------- END BAD EXAMPLES [DONT DO THIS] -----------

    {ovrd["FOOTER"]}

    """
