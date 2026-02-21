#!/usr/bin/env python

"""
The default config, wich will get partially or fully overwritten by the user config. 
"""

from __future__ import annotations
from typing import Literal, TypeAlias, TypedDict

from ai_diagnos_lsp.AnalysisSubsystem.AnalysisSubsystemClass import AnalysisSubsystemConfig
from ai_diagnos_lsp.AnalysisSubsystem.analysers.CrossFileAnalyser import CrossFileAnalysisConfig
from ai_diagnos_lsp.DiagnosticsHandlingSubsystem.main import DiagnosticsSubsystemConfig

LiteralSupportedAnalysisTypes: TypeAlias = Literal["Basic", "CrossFile", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle", "Deep", "Workspace"]
    

class __DefaultConfigType(TypedDict):
    
    timeout: int | float
    debounce_ms: int | float
    max_file_size: int
    show_progress: bool
    show_progress_every_ms: int | float
    ai_diagnostics_symbol: str

    use_omniprovider: bool

    use_gemini: bool
    model_gemini: str
    fallback_models_gemini: list[str] | None

    use_openrouter: bool
    model_openrouter: str

    use_groq: bool
    model_groq: str
    fallback_models_groq: list[str] | None

    use_cerebras: bool
    model_cerebras: str
    fallback_models_cerebras: list[str] | None

    api_key_huggingface: str
    model_huggingface: str

    AnalysisSubsystem: AnalysisSubsystemConfig
    CrossFileAnalysis: CrossFileAnalysisConfig
    DiagnosticsSubsystem: DiagnosticsSubsystemConfig

    plugins: dict[str, str]


class user_config(__DefaultConfigType):
    api_key_gemini: str
    api_key_openrouter: str
    api_key_groq: str
    api_key_cerebras: str

DEFAULT_CONFIG: user_config = {
    "timeout": 99999,
    "debounce_ms": 3000,
    "max_file_size": 10000,
    "show_progress": True,
    "show_progress_every_ms": 5000,
    "ai_diagnostics_symbol": "AI",

    "use_omniprovider": True,

    "use_gemini": False,
    "model_gemini": "gemini-2.5-pro",
    "fallback_models_gemini": [
        "gemini-2.5-flash", "gemini-3-flash-preview"
    ],

    "use_openrouter": False,
    "model_openrouter": "tngtech/tng-r1t-chimera:free",

    "use_groq": False,
    "model_groq": "openai/gpt-oss-120b",
    "fallback_models_groq": [
        "openai/gpt-oss-20b", "openai/gpt-oss-safeguard-20b", "qwen/qwen3-32b", "llama-3.3-70b-versatile"
    ], # AI diagnos lsp: This groq configuration was tested and proved to be functional. 

    "use_cerebras": True,
    "model_cerebras":  "openai/gpt-oss-120b",
    "fallback_models_cerebras": [ ],

    "AnalysisSubsystem": {
        "write": ["Basic", "CrossFile", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle"], 
        "open": ["Basic", "CrossFile", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle"],
        "change": [ ],
        "command": [ "CrossFile" ],
        "max_threads": 5,
    },
    "CrossFileAnalysis": {
        "scope": [ "~" ],
        "max_analysis_depth": None,
        "max_string_size_char": 1000000
    },
    "DiagnosticsSubsystem": {
        "check_ttl_for_deletion": 360,
        "sqlite_db_name": "diagnostics.db",
        "check_ttl_for_invalidation": 5,
        "ttl_until_deletion": 2592000,
        "ttl_until_invalidation": 15
    },
    "plugins": {
        ".py": "/the/example/path/for/ya/to/see/how/this/works"
    },
    'api_key_gemini': "",
    'api_key_groq': "",
    "api_key_openrouter": "",
    'api_key_cerebras': ""

}
