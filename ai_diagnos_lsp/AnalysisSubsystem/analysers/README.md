# analysers

The documentation and the specification of how analysers are built. 

## Architecture:

An analyser is basically a thread that assembles a langchain chain out of components under ´./chains/´ , and then just submits it to the correct chain invoker under ´utils/langchain´

The llm gets created by the function create llm with config from ´utils/langchain´. 

All the AI components are langchain, since this lsp uses langchain.

All the components are provided as factory functions, and must gotten from running the factories. 
Even if that is not nesesary, I still think that is the correct approach.

### Components

The LLMs are stored under ´chains/LLM/´. 
The prompt objects, in form of factory functions, are stored under ´chains/PromptObjects/´.

More on that in the dedicated file. 
TODO: ADD THE LINK TO HERE

### Contribution

Adding anouther LLM for anouther provider and wiring it in is pretty much a welcome PR. 

If you want to work with prompts, read their dedicated readme. 
TODO: ADD LINK TO IT HERE.
