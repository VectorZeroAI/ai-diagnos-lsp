# AI Diagnos LSP

A Python‑based Language Server that provides AI‑powered diagnostics using LangChain. It integrates with multiple LLM providers (Gemini, OpenRouter, Groq) and features semantic location matching, cross‑file analysis, and persistent diagnostic storage. Designed to be used with the [ai_diagnos.nvim](https://github.com/VectorZeroAI/ai_diagnos.nvim) plugin, but can be configured for any editor that supports the Language Server Protocol.

Is in active development, and still not release capable. For ifi

## Features

- **Pull‑based diagnostics** – diagnostics are requested on file open, save, or via custom commands.
- **Multiple LLM providers** – Gemini, OpenRouter, Groq, or an “Omniprovider” that falls back through them.
- **Semantic location matching** – locates issues by exact code snippet, reducing hallucinated line numbers.
- **Cross‑file analysis** – recursively resolves imports to provide additional context (currently Python‑only).
- **Diagnostics storage** – SQLite database caches results; configurable TTLs for invalidation and deletion.
- **Configurable analysis triggers** – which analysers run on `open`, `save`, `change`, or manual command.
- **Debouncing and file size limits** – prevents excessive API calls on large files or rapid edits.
- **Progress notifications** – optional periodic updates while the LLM is processing.
- **Custom LSP commands** – trigger analysis, clear diagnostics, etc.
- **omni language support** - LLM based analysis is omnilingual, the only changes that need to be done per language are the parsers, there is a nice plugin system to write yourself. ( Theres also a repo available for the parsers. TODO: Insert URL here)

## Requirements

- Python ≥ 3.9
- `pip` and `venv` (or `uv`)
- API keys for the chosen provider(s)

## Installation

The LSP is a Python package. You can install it from its repository:

```bash
# Clone the repository
git clone https://github.com/VectorZeroAI/ai-diagnos-lsp.git
cd ai-diagnos-lsp

# Install with pip
pip install .

# Or with uv (faster)
uv sync
uv pip install .
```

The server executable `ai-diagnos-lsp` will be placed in your Python environment’s `bin` directory.

## Configuration

The LSP accepts configuration via the `initializationOptions` field in the LSP `initialize` request. The options mirror those of the Neovim plugin. Below is the complete set of options with their types and defaults.

| Option                        | Type                | Default                                   | Description |
|-------------------------------|---------------------|-------------------------------------------|-------------|
| `api_key_openrouter`          | `string`            | –                                         | OpenRouter API key (required for OpenRouter or Omniprovider). |
| `api_key_gemini`              | `string`            | –                                         | Gemini API key (required for Gemini or Omniprovider). |
| `api_key_groq`                | `string`            | –                                         | Groq API key (required for Groq or Omniprovider). |
| `use_gemini`                  | `boolean`           | `false`                                   | Enable only Gemini. |
| `use_openrouter`              | `boolean`           | `false`                                   | Enable only OpenRouter. |
| `use_groq`                    | `boolean`           | `false`                                   | Enable only Groq. |
| `use_omniprovider`            | `boolean`           | `true`                                    | Try OpenRouter → Gemini → Groq. |
| `model_openrouter`            | `string`            | `"tngtech/tng-r1t-chimera:free"`          | Model name for OpenRouter. |
| `model_gemini`                | `string`            | `"gemini-2.5-flash-lite"`                 | Model name for Gemini. |
| `model_groq`                  | `string`            | `"openai/gpt-oss-120b"`                   | Model name for Groq. |
| `fallback_models_gemini`      | `array` of `string` | `["gemini-2.5-flash", "gemini-3-flash-preview"]` | Fallback models for Gemini. |
| `fallback_models_groq`        | `array` of `string` | `["openai/gpt-oss-20b", "openai/gpt-oss-safeguard-20b", "qwen/qwen3-32b", "llama-3.3-70b-versatile"]` | Fallback models for Groq. |
| `debounce_ms`                 | `integer`           | `3000`                                   | Minimum time (ms) between analyses for the same file. |
| `max_file_size`               | `integer`           | `10000`                                  | Maximum number of lines to analyse. Larger files are skipped. |
| `timeout`                     | `integer`           | `99999`                                  | Maximum wait time (seconds) for the LLM to respond. |
| `show_progress`               | `boolean`           | `true`                                   | Show periodic progress notifications. |
| `show_progress_every_ms`      | `integer`           | `5000`                                   | Interval between progress notifications. |
| `ai_diagnostics_symbol`       | `string`            | `"AI"`                                   | (Not used by LSP, but passed through.) |
| `AnalysisSubsystem`           | `object`            | See below                                | Controls which analyses run on which events. |
| `CrossFileAnalysis`           | `object`            | See below                                | Cross‑file analysis specific settings. |
| `DiagnosticsSubsystem`        | `object`            | See below                                | Database and TTL settings. |
| `plugins`        | `object`            | See below                                | Add your own parsers per language, to enable omnilang cross file diagnostics |

### AnalysisSubsystem

```json
{
  "write": ["CrossFile", "Basic"],
  "open": ["Basic", "CrossFile"],
  "change": [],
  "command": ["CrossFile"],
  "max_threads": 5
}
```

- `write`, `open`, `change`, `command`: lists of analysis types to run on each event. Supported types: `"Basic"`, `"CrossFile"`, `"Logic"`, `"Style"`, `"Security"`, `"Deep"` (only `Basic` and `CrossFile` are implemented so far).
- `max_threads`: maximum concurrent analysis threads.

### CrossFileAnalysis

```json
{
  "scope": ["/path/to/project/src"],
  "max_analysis_depth": null,
  "max_string_size_char": 1000000
}
```

- `scope`: list of directory paths that limit which imported files are included.
- `max_analysis_depth`: how deep to recursively follow imports (`null` = unlimited).
- `max_string_size_char`: maximum character length of the aggregated context.

### DiagnosticsSubsystem

```json
{
  "check_ttl_for_deletion": 360,
  "sqlite_db_name": "diagnostics.db",
  "check_ttl_for_invalidation": 5,
  "ttl_until_deletion": 2592000,
  "ttl_until_invalidation": 15
}
```

- `check_ttl_for_deletion`: seconds between checks for old files to delete.
- `sqlite_db_name`: database file name.
- `check_ttl_for_invalidation`: seconds between checks for stale diagnostics.
- `ttl_until_deletion`: seconds after last write before a file’s records are purged (default 30 days).
- `ttl_until_invalidation`: seconds after a file write before old diagnostics are considered stale and deleted.

> **Note**: Only **one** of `use_gemini`, `use_openrouter`, `use_groq`, or `use_omniprovider` should be `true` at a time. The Omniprovider is the default and requires all three API keys (they can be empty strings to skip that provider).

### plugins

Currently it is basically a dict of file extension (e.g. ".py") and paths to the parsers.
I dont think I need a table to explain that. 

For info on how to write one, look in the parser protocol section under Contribution. 

## Architecture

The server is built with [`pygls`](https://pygls.readthedocs.io/) and organised into several subsystems:

- **`AIDiagnosLSP`** – main server class, inherits from `LanguageServer`. Holds configuration, diagnostics cache, and references to subsystems.
- **`AnalysisSubsystem`** – manages analysis requests. Uses a `ThreadPoolExecutor` to run analysers concurrently, respects debounce and file size limits, and dispatches to the appropriate analyser based on the event.
- **Analysers** – currently `BasicDiagnoseFunctionWorker` (single‑file analysis) and `CrossFileAnalyserWorkerThread` (cross‑file). Each builds a LangChain (prompt + LLM + output parser) and invokes it in a separate thread.
- **`DiagnosticsHandlingSubsystem`** – persistent storage via SQLite. Stores diagnostics per file per analysis type, with timestamps. Provides methods to save new diagnostics, load them for a file, and background threads for TTL‑based cleanup.
- **Utility modules** – `grep.py` for exact snippet matching, `parser.py` for Python import resolution.

### Data flow

1. Client sends a text document event (`didOpen`, `didSave`, `didChange`) or a custom `workspace/executeCommand`.
2. Server calls `AnalysisSubsystem.submit_document_for_analysis(doc, event)`.
3. Subsystem checks debounce, file size, and launches the required analysers in a thread pool.
4. Analyser builds the appropriate chain and invokes the LLM.
5. LLM returns a JSON‑formatted list of diagnostics (using the Pydantic model `GeneralDiagnosticsPydanticObjekt`).
6. Analyser calls `DiagnosticsHandlingSubsystem.save_new_diagnostic()` to store the result.
7. It then calls `load_diagnostics_for_file()` which retrieves all stored diagnostics for that file, converts them to LSP `Diagnostic` objects (using snippet matching via `grep`), and updates the server’s in‑memory cache.
8. Finally, the server sends a `workspace/diagnostic/refresh` request to notify the client to pull updated diagnostics.

## LSP Methods

The server implements the following LSP methods:

- `initialize` – stores the configuration from `initializationOptions`.
- `initialized` – initialises subsystems and loads all stored diagnostics.
- `textDocument/didOpen` – attempts to load cached diagnostics; if none, triggers analysis.
- `textDocument/didChange` – reloads diagnostics from cache (can be configured to trigger analysis).
- `textDocument/didSave` – registers a file write and triggers analysis.
- `textDocument/diagnostic` – returns diagnostics for a specific document (pull model).
- `workspace/diagnostic` – returns diagnostics for the whole workspace.
- `workspace/executeCommand` – supports custom commands:
  - `Analyse.Document` – expects a URI parameter; forces analysis.
  - `Clear.AIDiagnostics` – clears diagnostics for a given URI.
  - `Clear.AIDiagnostics.All` – clears all diagnostics.

## Troubleshooting

Set the environment variable `AI_DIAGNOS_LOG=1` to enable detailed logging to `ai_diagnos_lsp.log` in the working directory.

BE AWARE THAT THE LOG LOGS THE API KEYS PLAINTEXT

Common issues:

- **Server fails to start**: Ensure all required API keys are provided and the Python environment has the necessary packages.
- **No diagnostics appear**: Check that the file type is supported (the client must request diagnostics; the LSP only responds to pull requests). Verify that the file size is below `max_file_size` and that debounce is not suppressing the request.
- **LLM errors**: Inspect the log for API errors or timeouts. Verify that the model names are correct and the API keys have access.


## Contributions

Contributions are welcome - especially new parsers
I will be creating a repo as a way to distribute the plugin parsers.
TODO : Dont forget to add the repo here. 

### Parser Protocol

In this section, I will explain the protocol I have designed for the plugin parsers. 

A plugin parser is a single executable that acts as a parser function, that gets the file in, and returns the list of files that the file import back.
Limited to the project scope defined in the request. 

Communication happends over stdin / out. 

input: 
```json
{
    "project_scope": ["dir_name", "anouther_dir_name", "..."],
    "file_content": ["line_content", "anouther_line_content", "..."],
    "solid_file_content": "The whole file content as one string",
    "file_path": "/file/path"
}
```

output:
```json
[
    "file_imported_1", "file_imported_2", "file_imported_3"
]
```

> [!NOTE]
> stdin is not the same as args field as far as I know. 

## License

[MIT](LICENSE)
