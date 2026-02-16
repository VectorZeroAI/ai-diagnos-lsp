#!/usr/bin/env python3

from typing import List, TypedDict, Any
from pygls.lsp.server import LanguageServer
import os
import logging
import threading

from ai_diagnos_lsp.DiagnosticsHandlingSubsystem.main import DiagnosticsHandlingSubsystemFactory
from ai_diagnos_lsp.AnalysisSubsystem.AnalysisSubsystemClass import AnalysisSubsystemClassFactory
from ai_diagnos_lsp.AnalysisSubsystem.AnalysisSubsystemClass import AnalysisSubsystemConfig

class config(TypedDict):
    timeout: int | float
    debounce_ms: int | float
    max_file_size: int
    show_progress: bool
    show_progress_every_ms: int | float
    ai_diagnostics_symbol: str

    use_omniprovider: bool

    api_key_gemini: str
    api_key_openrouter: str
    api_key_groq: str

    use_gemini: bool
    model_gemini: str
    fallback_models_gemini: List[str]

    use_openrouter: bool
    model_openrouter: str

    use_groq: bool
    model_groq: str
    fallback_models_groq: List[str]

    AnalysisSubsystem: AnalysisSubsystemConfig

class AIDiagnosLSP(LanguageServer):
    """
    My language server class. 
    It is pull diagnostics based. 
    """

    SUPPORTED_DIAGNOSTIC_TYPES = ["Basic", "CrossFile", "Logic", "Style", "Security", "Deep"]

    def __init__(self, *args, **kwargs): # pyright: ignore
        super().__init__(*args, **kwargs) # pyright: ignore
        if os.getenv("AI_DIAGNOS_LOG") is not None:
            logging.basicConfig(
                    filename="ai_diagnos_lsp.log",
                    level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%H:%M:%S'
                    )

        self.diagnostics: dict[str, tuple[int | Any] | tuple[None, None]] = {}
        self.last_diagnostic_time = {}
        self.config: config = {} # pyright: ignore
        self.diagnostics_lock = threading.Lock()

    def init_subsystems(self) -> None:
        self.DiagnosticsHandlingSubsystem = DiagnosticsHandlingSubsystemFactory(self)
        self.AnalysisSubsystem = AnalysisSubsystemClassFactory(self)

