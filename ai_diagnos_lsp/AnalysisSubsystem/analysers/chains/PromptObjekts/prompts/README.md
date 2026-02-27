# prompts

This is the directory where the prompts are located. 

## Architecture

The prompts are split into [SHARED.py](./SHARED.py), and [EXEMPLARS.py](./EXEMPLARS.py).
The prompts are based on rule based directives, and In Context Learning for everything else.
The actual prompts are just assembling the parts from the SHARED and EXEMPLARS files. 

## Reference:

Look up the prompt report on arxiv, and its related works, that is some good stuff there. I referenced that myself. 

## Contributing

This part needs a lot of contributions. 
Things I want to do / plan to do:
1. Cut the prompts size
2. Make the AI stop forgetting to close the thinking step
3. Improve models performance by altering the chain of thought exemplars to be more effective

Just though a PR with the changes, I will merge it, or say what was done wrong. 
