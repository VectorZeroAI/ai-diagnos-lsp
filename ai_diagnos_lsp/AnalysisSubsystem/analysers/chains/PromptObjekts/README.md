# Prompt Objects

This is the directory for prompt objects. 

Each prompt is a factory function, because there is a feature of overridability of the parts of the prompts. 
That requires computing the overrides for the prompt right before creation of the prompt object, wich makes a factory function actually good design. 

## Prompt Overrides
The overriding is structured as following: the user config @ prompt_overrides @ file suffix = path of the python file of the overrides. 
Then each element from inside SHARED and EXEMPLARS ([details here](./prompts/README.md)) is extracted and inputed, if one is present, else the default located at SHARED or EXEPLARS is inputed into the system prompt. 

An example override file would look like this: 
```python
GOOD_EXAMPLES = """
{
    "diagnostics": [
        {
            "start": "example",
            "end": "example",
            "error_message": "example",
            ...
        }
    ]
}
"""
```

For the full list of all the overridable parts of the prompt, see the table under [here](./prompts/README.md).

## Contribution

If you are willing to contribute to prompts, read the [actual prompts readme here](./prompts/README.md).
If you find anything worthy to contribute here, then just do however you want to.
