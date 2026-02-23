# Analysis Subsystem

The analysis subsystem doc. 

## Usage

Submit document for analysis call. Everything else is handeled by the configuration.

## Configuration

```json
{
    "write": ["CrossFile", "Basic", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle"],
    "open": ["Basic", "CrossFile", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle"],
    "change": ["Basic", "CrossFile", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle"],
    "command": ["CrossFile"],
    "max_threads": 5
}
```

Those are the currently supported analysers. 

Planned: Deep and Workspace and their variants. 


## Contributing

If you have any good ideas, open an issue. 
Dont just through a PR without an issue onto here, this is a core. 
