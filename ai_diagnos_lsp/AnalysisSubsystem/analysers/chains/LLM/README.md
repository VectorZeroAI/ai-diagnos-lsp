# LLM parts

This is the directory for the LLM parts.

All of those are to be initiated via Factory functions first, and only then be actually used. 

## Architecture

There is the `__init__.py` file wich serves no purpose. 

There are the per provider LLMs that follow pretty much the same architecture: 

**Factory function**: 
    **input**:
    - api_key
    - model
    - fallback_model [fully optional]
    **output**:
    - the langchain llm object, e.g. langchain runnable that calls the API (optionally with fallbacks)

And there is the omniprovider LLM, wich basically chains every Provider as the fallbacks, optionally with their own fallbacks, to form a giant chain of LLMs. (For the purpose of doging ratelimits)

