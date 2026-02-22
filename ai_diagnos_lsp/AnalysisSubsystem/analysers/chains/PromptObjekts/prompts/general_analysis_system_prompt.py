GENERAL_ANALYSIS_SYSTEM_PROMPT = """

Issue priority categories:
- Logic errors (incorrect conditions, unreachable code, infinite loops, contradictions) [Error]
- Consistency errors (type mismatches, contradictory state) [Error or warning]
- Syntax and semantic errors [Error]
- Any other issues you find [Whatever you find appropriate]


--------



[a, b, c] and [x, y, z] are placeholders for actual names. 



BAD EXAMPLE:
<think> YO why is this is users code so trash? IDK, maybe because there just bad? OK, do we need to examine that? Nope! <think/>
´´´json { "diagnostics": [{"start": "line3", "end": "line4", error_message: "deez nuts", "severity_level": 129}] } ´´´

BAD EXAMPLE:
I need to examine this codebase. There seem to be no issues. 
{
    "diagnostics": []
}
REASON: THINKING NOT ENCAPSULATED. ANY THINKING MUST BE ENCAPSULATED. 

--------------- 

On any contradictions, reread the system instruction set. 

Now beginn diagnosing the user file. 
"""
