#!/usr/bin/env python

"""
The default config, wich will get partially or fully overwritten by the user config. 
"""

from __future__ import annotations
from typing import Literal, TypedDict

from ai_diagnos_lsp.AnalysisSubsystem.AnalysisSubsystemClass import AnalysisSubsystemConfig
from ai_diagnos_lsp.AnalysisSubsystem.analysers.CrossFileAnalyser import CrossFileAnalysisConfig
from ai_diagnos_lsp.DiagnosticsHandlingSubsystem.main import DiagnosticsSubsystemConfig

LiteralSupportedAnalysisTypes = Literal["Basic", "CrossFile", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle", "Deep", "Workspace"]
LiteralSupportedProviders = Literal["Openrouter", "Omniprovider", "Claude", "OpenAI", "gemini", "groq", "cerebras", "huggingface"]

SUPPORTED_DIAGNOSTIC_TYPES = ["Basic", "CrossFile", "BasicLogic", "CrossFileLogic", "BasicStyle", "CrossFileStyle", "Deep"] 

class __DefaultConfigType(TypedDict):
    
    timeout: int | float
    debounce_ms: int | float
    max_file_size: int
    show_progress: bool
    show_progress_every_ms: int | float

    use: LiteralSupportedProviders

    model_gemini: str
    fallback_models_gemini: list[str] | None

    model_openrouter: str

    model_groq: str
    fallback_models_groq: list[str] | None

    model_cerebras: str
    fallback_models_cerebras: list[str] | None

    model_huggingface: str

    model_openai: str

    model_claude: str

    AnalysisSubsystem: AnalysisSubsystemConfig
    CrossFileAnalysis: CrossFileAnalysisConfig
    DiagnosticsSubsystem: DiagnosticsSubsystemConfig

    plugin_parsers: dict[str, str]
    prompt_overrides: dict[str, str]

class user_config(__DefaultConfigType):
    api_key_gemini: str
    api_key_openrouter: str
    api_key_groq: str
    api_key_cerebras: str
    api_key_huggingface: str
    api_key_openai: str
    api_key_claude: str

DEFAULT_CONFIG: user_config = {
    "timeout": 99999,
    "debounce_ms": 3000,
    "max_file_size": 10000,
    "show_progress": True,
    "show_progress_every_ms": 5000,

    "use": "Omniprovider",

    "model_gemini": "gemini-2.5-pro",
    "fallback_models_gemini": [
        "gemini-2.5-flash", "gemini-3-flash-preview", "gemma-3-27b-it"
    ],

    "model_openrouter": "tngtech/tng-r1t-chimera:free",

    "model_huggingface": "Qwen2.5-Coder-7B-Instruct",
    "model_openai": "",
    "model_claude": "",

    "model_groq": "openai/gpt-oss-120b",
    "fallback_models_groq": [
        "openai/gpt-oss-20b", "openai/gpt-oss-safeguard-20b", "qwen/qwen3-32b", "llama-3.3-70b-versatile"
    ],

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
    "plugin_parsers": {
        ".py": "/the/example/path/for/ya/to/see/how/this/works"
    },
    "prompt_overrides": {
        ".example": "/the/example/path/to/overrides.py"
    },
    'api_key_gemini': "",
    'api_key_groq': "",
    "api_key_openrouter": "",
    'api_key_cerebras': "",
    "api_key_huggingface": "",
    'api_key_claude': "",
    'api_key_openai': ""

}
