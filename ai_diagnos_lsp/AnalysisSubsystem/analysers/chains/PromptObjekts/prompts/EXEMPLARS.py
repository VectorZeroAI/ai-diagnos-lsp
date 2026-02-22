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
```json
{
"diagnostics": []
}
```
"""


COT_EXAMPLES = """
GOOD EXAMPLE:
<think>Lets examine the code step by step first. What language is this code? Its abc? Is it? Yes it is. 
Okay, we determined that the language is abc. Now, lets move on the the import section. Does it look correct?
Yes it does. Is it though? No it isnt, because in the abc language imports can not be xyz. Is that fact true though?
Should this be included in the final diagnostic? Yes it should. But at what severity level?
2. Why? Because the system prompt says that we should mark syntax errors as 1, wait so actually 1? Yes, actually it says syntax errors go to severity level one.
Did we make a mistake? No we didnt. Lets now move on to the next section of the file.</think>

GOOD EXAMPLE:
<think>Lets examine the code step by step first. What language is this code? Its abc? Is it? Yes it is. 
Okay, we determined that the language is abc. Now, lets move on the the import section. Is the syntax there correct?
Yes it is. We notice that the user import the library b. Do we know about the library? Yes. What is the library? Actually we dont. 
Wait, so we dont? Lets take a step back and take a different approach. So we see the user import that library,
we dont know what that library is, so, is it part of stdlib? No. Why? Wait, actually yes. Why? Wait actually we dont know.
Lets take a different approch. As we know, we dont know what the library is, so it potentially doesnt exist.
Lets put it exactly like that into the final diagnostic.</think>

GOOD EXAMPLE:
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

GOOD EXAMPLE:
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
Should we write the diagnostic? Yes we should.<think/>
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
