GOOD_EXAMPLES = """
EVERY EXAMPLE BELOW FOLLOWS THIS STRUCTURE:

<think>
[YOUR ACTUAL REASONING GOES HERE - THIS IS A PLACEHOLDER]
</think>
{ "diagnostics": [...] }

THE PLACEHOLDER ABOVE REPRESENTS MANDATORY COMPREHENSIVE REASONING.
DO NOT output JSON without first completing a thorough think block like the one above.
DO NOT write short or superficial thinking. The quality of diagnostics depends on the depth of reasoning.

-------- GOOD EXAMPLE (single-line span, severity 1 ERROR - contradictory condition): --------
<think>...</think>
{
"diagnostics": [
    {
        "start": "if user_age < 0 and user_age > 150:",
        "end": "if user_age < 0 and user_age > 150:",
        "error_message": "Contradictory condition: a value cannot be simultaneously less than 0 and greater than 150. This branch is unreachable.",
        "severity_level": 1
    }
]
}

-------- GOOD EXAMPLE (multi-line span, severity 1 ERROR - variable used before assignment): --------
<think>...</think>
{
"diagnostics": [
    {
        "start": "def process_order(cart):",
        "end": "return total_price",
        "error_message": "'total_price' is used in the return statement but is only assigned inside the 'if cart:' branch. If cart is empty or falsy, total_price will be undefined at the return.",
        "severity_level": 1
    }
]
}

-------- GOOD EXAMPLE (occurrence index - targeting a repeated token): --------
If a snippet appears more than once in the file, specify which occurrence using ["snippet", N] where N is 1-based.
<think>...</think>
{
"diagnostics": [
    {
        "start": ["except Exception:", 2],
        "end": ["except Exception:", 2],
        "error_message": "Bare 'except Exception' silently swallows all errors. Catch specific exception types instead, or at minimum log the error before continuing.",
        "severity_level": 2
    }
]
}
This targets the SECOND occurrence of 'except Exception:' in the file, not the first.

-------- GOOD EXAMPLE (all four severity levels - one diagnostic per level): --------
<think>...</think>
{
"diagnostics": [
    {
        "start": "if user_count < 0 and user_count > 1000:",
        "end": "if user_count < 0 and user_count > 1000:",
        "error_message": "Contradictory condition: user_count cannot be simultaneously less than 0 and greater than 1000. This branch is unreachable.",
        "severity_level": 1
    },
    {
        "start": "result = db.find_user(user_id)",
        "end": "print(result.name)",
        "error_message": "db.find_user() can return None but result.name is accessed without a None check. This will raise AttributeError if the user is not found.",
        "severity_level": 2
    },
    {
        "start": "def Calculate_Total(ItemList):",
        "end": "def Calculate_Total(ItemList):",
        "error_message": "Function name 'Calculate_Total' and parameter 'ItemList' use PascalCase. PEP8 convention for Python functions and parameters is snake_case (calculate_total, item_list).",
        "severity_level": 3
    },
    {
        "start": "results = []",
        "end": "return results",
        "error_message": "This pattern (initialise empty list, append in loop, return) can be expressed more concisely as a list comprehension, which is also faster.",
        "severity_level": 4
    }
]
}

-------- GOOD EXAMPLE (no issues found - output exactly this): --------
<think>...</think>
{
"diagnostics": []
}
"""

BAD_EXAMPLES = """
-------- BAD EXAMPLE (markdown code fences are forbidden): --------
```json
{
"diagnostics": [
    {
        "start": "some_function()",
        "end": "some_function()",
        "error_message": "some issue",
        "severity_level": 1
    }
]
}
```
Do NOT wrap output in ```json ... ``` or any other markdown fence.

-------- BAD EXAMPLE (invented or paraphrased snippet - start/end must be exact copies from the source): --------
{
"diagnostics": [
    {
        "start": "the loop on line 42",
        "end": "end of loop",
        "error_message": "off by one error",
        "severity_level": 1
    }
]
}
'start' and 'end' must be verbatim code copied character-for-character from the file, not descriptions or paraphrases.

-------- BAD EXAMPLE (two separate errors merged into one diagnostic): --------
{
"diagnostics": [
    {
        "start": "def process():",
        "end": "return result",
        "error_message": "Missing null check on input AND function lacks a docstring.",
        "severity_level": 2
    }
]
}
Each diagnostic must describe exactly one issue. Split the above into two separate diagnostic objects.

-------- BAD EXAMPLE (anything outside the JSON object): --------
Here are the diagnostics I found:
{
"diagnostics": []
}
Output must be the JSON object and nothing else. No preamble, no explanation, no sign-off.
-------- BAD EXAMPLE (broken thinking bracets) --------
</think>{
    "diagnostics": []
}
"""

COT_EXAMPLES = """
-------- GOOD EXAMPLE --------
<think>Lets examine the code step by step first. What language is this code? Its abc? Is it? Yes it is. 
Okay, we determined that the language is abc. Now, lets move on the the import section. Does it look correct?
Yes it does. Is it though? No it isnt, because in the abc language imports can not be xyz. Is that fact true though?
Should this be included in the final diagnostic? Yes it should. But at what severity level?
2. Why? Because the system prompt says that we should mark syntax errors as 1, wait so actually 1? Yes, actually it says syntax errors go to severity level one.
Did we make a mistake? No we didnt. Lets now move on to the next section of the file.</think>
{
    "diagnostics": [
        {
            "start": "import xyz",
            "end": "import xyz",
            "error_message": "Invalid import: abc language does not allow importing 'xyz'.",
            "severity_level": 1
        }
    ]
}

-------- GOOD EXAMPLE -------- 
<think>Lets examine the code step by step first. What language is this code? Its abc? Is it? Yes it is. 
Okay, we determined that the language is abc. Now, lets move on the the import section. Is the syntax there correct?
Yes it is. We notice that the user import the library b. Do we know about the library? Yes. What is the library? Actually we dont. 
Wait, so we dont? Lets take a step back and take a different approach. So we see the user import that library,
we dont know what that library is, so, is it part of stdlib? No. Why? Wait, actually yes. Why? Wait actually we dont know.
Lets take a different approch. As we know, we dont know what the library is, so it potentially doesnt exist.
Lets put it exactly like that into the final diagnostic.</think>
{
    "diagnostics": [
        {
            "start": "import b",
            "end": "import b",
            "error_message": "Unknown library 'b': this module is not recognized as part of the standard library and may not exist.",
            "severity_level": 3
        }
    ]
}

-------- GOOD EXAMPLE -------- 
<think>
First, let's identify what we are examining. This appears to be a code snippet written in the abc language. We need to analyze it for potential issues step by step.
Now, look at the first line: import xyz. In abc, imports are only allowed for modules that are part of the standard library or explicitly declared. Is xyz a standard module? I recall that the abc standard library includes modules like abc_base, but xyz is not among them. Could it be a third-party module? In abc, third-party modules require a module declaration at the top, which is missing here. So this import is likely invalid—a potential error, but not a syntax error.
Next, we see a function definition: def calculate(param):. The following line is result = param * 2. In abc, indentation is mandatory to define the body of a function. This line is not indented, so it is a syntax error. That means the function definition is malformed.
Then, we have return result on the next line, also without indentation. That's another syntax error within the same function. Because the function body is not properly indented, the function will not be defined correctly.
After that, there is a line print(calculate(5)) at the top level. That is fine syntactically, but it attempts to call calculate, which we already know is not properly defined due to the syntax errors. So even if we fix the indentation, this call might work, but currently it's part of a broken program.
Then we see print(value). Is value defined anywhere? Scanning the code, there is no assignment to value. This will cause a runtime error (NameError) if the program gets that far. So this is a logical error.
Finally, there is an if statement: if condition: followed by print('Hello') without indentation. In abc, the body of an if must be indented. This is another syntax error. Additionally, condition is not defined, which would be a logical error if the syntax were fixed.
Now, let's assess severity. According to the guidelines, syntax errors are level 1 (critical), logical errors like undefined variables are level 2, and potential missing imports are level 3 (warnings). We have multiple syntax errors: the missing indentation in the function and in the if statement. These prevent the code from even being parsed. Therefore, they are the highest priority.
The undefined variables (value and condition) are secondary—they would only matter after syntax errors are resolved. The import issue is a warning.
So the final diagnostic should highlight the syntax errors first. The code cannot run until those are fixed. After that, the undefined variables need to be addressed, and the import might be a note.
</think>
{
    "diagnostics": [
        {
            "start": "import xyz",
            "end": "import xyz",
            "error_message": "Unknown import 'xyz': not found in standard library; third-party modules require an explicit module declaration.",
            "severity_level": 3
        },
        {
            "start": "result = param * 2",
            "end": "return result",
            "error_message": "Syntax error: function body must be indented in abc. Lines inside 'calculate' are not indented.",
            "severity_level": 1
        },
        {
            "start": "print('Hello')",
            "end": "print('Hello')",
            "error_message": "Syntax error: body of 'if' block must be indented.",
            "severity_level": 1
        },
        {
            "start": "print(value)",
            "end": "print(value)",
            "error_message": "Logical error: 'value' is referenced but never defined.",
            "severity_level": 2
        },
        {
            "start": "if condition:",
            "end": "if condition:",
            "error_message": "Logical error: 'condition' is referenced but never defined.",
            "severity_level": 2
        }
    ]
}

------ GOOD EXAMPLE: -------
<think>Lets walk through the code line by line!
First, lets look at the import section of the provided file.
We see that it imports modules x, y, z that we can have in our context,
and it also imports a third party library called abc.
Do we know that library? Yes we do.
Okay, we finished walking through the import steps? No we didnt, we did not examine the shebang.
Ok, lets look at the shebang. Is the shebang correct? Yes it is.
Are we now finished with the import section of the file? Yes we are. 
So, next the user defines the function x that takes in the inputs y and z of types a and b. 
Did we read it correcty? No we didnt. Why? Actually, we did. 
Now lets move to the function body. First the user does a with the input z. Is that correct? Yes it is.
Why? Oh wait, it actually isnt correct, because the the type of z does not contain that method. Is that correct? No it isnt. 
Wait, it is. Wait, it isnt. Are we sure? No, because we cant decide. We are not sure, but a potential issue is still an issue? Is it ?
No it isnt, wait it is? What does the system prompt say about that? It doesnt specify anything.
Lets mark the issue as severity level 3, and move on. Is there anything left to unexamined? No there isnt.
Should we write the diagnostic? Yes we should.
</think>
{
    "diagnostics": [
        {
            "start": "z.a",
            "end": "z.a",
            "error_message": "potenially non-existant attribute access. Please double check if that is correct.",
            "severity_level": 3
        }
    ]
}
"""

