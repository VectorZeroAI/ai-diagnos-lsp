GOOD_EXAMPLES = """
--------
GOOD EXAMPLE:
{
"diagnostics": [
    {
        "start": "The small wrong spot",
        "end": "The small wrong spot",
        "error_message": "Explanation of what is wrong there",
        "severity_level": 1
    },
    {
        "start": "A big wrong spot start",
        "end": "A big wrong spot end",
        "error_message": "Explanation of what is wrong there",
        "severity_level": 2
    }
]
}
-------
GOOD EXAMPLE:
{
"diagnostics": [
    {
        "start": "if (x > 10 && x < 5)",
        "end": "&& y < 5)",
        "error_message": "Logic error: condition can never be true (x cannot be simultaneously greater than 10 and less than 5)",
        "severity_level": 1
    }
]
}
-------
If a location occurs multiple times, you must specify which occurrence you mean, like this: 
GOOD EXAMPLE:
{
"diagnostics": [
    {
        "start": ["de grep():", 2],
        "end": ["de grep():", 2],
        "error_message": "misspelled def keyword inside function definition",
        "severity_level": 1
    }
]
}
This example means the second occurrence of the "de grep():" pattern inside the code file. 
------
If you dont find any issues, output exactly this:
GOOD EXAMPLE:
{
"diagnostics": []
}
"""


BAD_EXAMPLES = """
BAD EXAMPLE:
´´´json
{
"diagnostics": []
}
´´´
------
BAD EXAMPLE:
{}
"""


COT_EXAMPLES = """
"""
