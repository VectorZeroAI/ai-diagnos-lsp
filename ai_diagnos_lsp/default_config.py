#!/usr/bin/env python

"""
The default config, wich will get partially or fully overwritten by the user config. 
"""

from __future__ import annotations
from typing import Literal, TypeAlias, TypedDict

from ai_diagnos_lsp.AnalysisSubsystem.AnalysisSubsystemClass import AnalysisSubsystemConfig
from ai_diagnos_lsp.AnalysisSubsystem.analysers.CrossFileAnalyser import CrossFileAnalysisConfig

LiteralSupportedAnalysisTypes: TypeAlias = Literal["Basic", "CrossFile", "Logic", "Style", "Security", "Deep"]
    

class DefaultConfigType(TypedDict):
    
    timeout: int | float
    debounce_ms: int | float
    max_file_size: int
    show_progress: bool
    show_progress_every_ms: int | float
    ai_diagnostics_symbol: str
    #------
    use_omniprovider: bool
    #------
    use_gemini: bool
    model_gemini: str
    fallback_models_gemini: list[str]
    #------
    use_openrouter: bool
    model_openrouter: str
    #------
    use_groq: bool
    model_groq: str
    fallback_models_groq: list[str]
    AnalysisSubsystem: AnalysisSubsystemConfig
    CrossFileAnalysis: CrossFileAnalysisConfig


class user_config(DefaultConfigType):
    api_key_gemini: str
    api_key_openrouter: str
    api_key_groq: str

DEFAULT_CONFIG: DefaultConfigType = {
    "timeout": 99999,
    "debounce_ms": 3000,
    "max_file_size": 10000,
    "show_progress": True,
    "show_progress_every_ms": 5000,
    "ai_diagnostics_symbol": "AI",

    "use_omniprovider": True,

    "use_gemini": False,
    "model_gemini": "gemini-2.5-flash-lite",
    "fallback_models_gemini": [
        "gemini-2.5-flash", "gemini-3-flash-preview", "gemini-2.5-pro"
    ],

    "use_openrouter": False,
    "model_openrouter": "tngtech/tng-r1t-chimera:free",

    "use_groq": False,
    "model_groq": "openai/gpt-oss-120b",
    "fallback_models_groq": [
        "openai/gpt-oss-20b", "openai/gpt-oss-safeguard-20b", "qwen/qwen3-32b", "llama-3.3-70b-versatile"
    ],

    "AnalysisSubsystem": {
        "write": [ "CrossFile", "Basic" ],
        "open": [ "Basic", "CrossFile" ],
        "change": [ ],
        "command": [ "CrossFile" ],
        "max_threads": 5,
    },
    "CrossFileAnalysis": {
        "scope": [ "Nope. Fo put that in yourself. This is here for keyerrors to not occur. " ],
        "max_analysis_depth": None,
        "max_string_size_char": 1000000
    }
}
