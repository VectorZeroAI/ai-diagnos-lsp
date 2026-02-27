# chains

This is the chains directory, basically the place to put all the langchain chain parts into. 

There are the subdirectories LLM and PromptObjects.

## Architecture

./
    LLM/
        the_llms_and_parts
    PromptObjects/
        the_prompts_per_analyser
    DiagnosticsObjects/
        the_diagnostics_objects

> [!NOTE]
> Because currently only one diagnostics object exists, I did not yet create the directory for them. Once there are move, I will immidiately create the directory.

> [!NOTE]
> Factory function everything for scalability and style!
