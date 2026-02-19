#!/usr/bin/env python3

from typing import Any
from pygls.lsp.server import LanguageServer
import os
import logging
import threading

from ai_diagnos_lsp.DiagnosticsHandlingSubsystem.main import DiagnosticsHandlingSubsystemFactory
from ai_diagnos_lsp.AnalysisSubsystem.AnalysisSubsystemClass import AnalysisSubsystemClassFactory
from ai_diagnos_lsp.default_config import DefaultConfigType

class AIDiagnosLSP(LanguageServer):
    """
    My language server class. 
    It is pull diagnostics based. 
    """

    SUPPORTED_DIAGNOSTIC_TYPES = ["Basic", "CrossFile", "Logic", "Style", "Security", "Deep"]
    # NOTE : DONT FORGET TO UPDATE THE DEFAULT CONFIG WITH THE NEW DEFINITION AFTER EACH CHANGE

    def __init__(self, *args, **kwargs): # pyright: ignore
        super().__init__(*args, **kwargs) # pyright: ignore
        if os.getenv("AI_DIAGNOS_LOG") is not None:
            logging.basicConfig(
                    filename="ai_diagnos_lsp.log",
                    level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%H:%M:%S'
                    )

        self.diagnostics: dict[str, tuple[int | Any, Any] | tuple[None, None]] = {}
        self.last_diagnostic_time = {}
        self.config: DefaultConfigType = {} # pyright: ignore
        self.diagnostics_lock = threading.Lock()

    def init_subsystems(self) -> None:
        self.DiagnosticsHandlingSubsystem = DiagnosticsHandlingSubsystemFactory(self)
        self.AnalysisSubsystem = AnalysisSubsystemClassFactory(self)

