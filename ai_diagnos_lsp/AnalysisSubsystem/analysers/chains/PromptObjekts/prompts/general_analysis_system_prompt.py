from .SHARED import FOOTER, FORMAT_DESC, IDENTITY, LOGIC_ERRORS_DESC, CONSISTENCY_ERROR_DESC, TASK
from .EXEMPLARS import BAD_EXAMPLES, COT_EXAMPLES, GOOD_EXAMPLES

GENERAL_ANALYSIS_SYSTEM_PROMPT = f"""
{IDENTITY}

{TASK}

Issue priority categories:
- Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions) [Error]
- Consistency errors (type mismatches, contradictory state) [Error or warning]
- Syntax and semantic errors [Error]
- Any other issues you find [Whatever you find appropriate]

{LOGIC_ERRORS_DESC}

{CONSISTENCY_ERROR_DESC}

{FORMAT_DESC}

------ BEGINN EXAMPLES --------

{GOOD_EXAMPLES}

---------

{COT_EXAMPLES}

------- END EXAMPLES ----------

------- BEGINN BAD EXAMPLES [DONT DO THIS] --------

{BAD_EXAMPLES}

------- END BAD EXAMPLES [DONT DO THIS] -----------

{FOOTER}

"""
