#!/usr/bin/env python
from __future__ import annotations
from typing import TYPE_CHECKING, Literal

from pygls.workspace import TextDocument

if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import time
from lsprotocol import types

from ai_diagnos_lsp.AnalysisSubsystem.analysers.BasicDiagnoseFunction import BasicDiagnoseFunctionWorker

class AnalysisSubsystem:
    """
    The Analysis handling subsystem. 
    Is an abstraction layer between raw analysis worker threads and the lsp side callers. 
    The lsp side callers just submit the document and the event to this subsystem, wich handeles everything else. 
    
    Functionality includes:
        debounce time
        optional cancelation
        status gathering
        max_file_size checks. 
        Capping the amount of threads. 

    Configuration is the following:
        ["AnalysisSubsystem"][event] = ["analysis_types", "list"]
    """
    def __init__(self, ls: AIDiagnosLSP) -> None:
        self.ls = ls
        self.config = ls.config["AnalysisSubsystem"]
        self.executor = ThreadPoolExecutor(max_workers=self.config["max_threads"])
        self.submited_analyses = {}
        self.last_analysed_at = {}

    def submit_document_for_analysis(self,
                                     doc: TextDocument | Path,
                                     event: Literal["write", "open", "change"]
                                     ):
        """
        This is the document submission for diagnostics function. 
        It takes in the document, ether TextDocument or Path object, 
        and the event on wich it was called. 

        Then it checks for debounce time and max_file_size, and then submits the raw worker thread to the 
            executor.

        To understand what analysers to submit, it does pattern matching over the configuration. 
        """

        for i in self.ls.SUPPORTED_DIAGNOSTIC_TYPES:
            self.submited_analyses[i] = {}

        if type(doc) is TextDocument:
            uri = doc.uri
        elif type(doc) is Path:
            uri = doc.as_uri()
        else:
            raise TypeError(f"Invalid input type on doc parameter. Got {doc} of type {type(doc)}, expected object of type TextDocument or Path")
        
        if "Basic" in self.config[event]:
            if time.time() - self.last_analysed_at["Basic"][uri] < self.ls.config["debounce_ms"]:
                self.submited_analyses["Basic"][uri] = self.executor.submit(BasicDiagnoseFunctionWorker, doc, self.ls)
                self.last_analysed_at["Basic"][uri] = time.time()
            else:
                self.ls.window_show_message()

        if "CrossFile" in self.config[event]:
            raise NotImplementedError("Cross file diagnostics not yet implemented")
            #self.submited_analyses["CrossFile"][uri] = self.executor.submit(CrossFileDiagnoseFunctionWorker, doc, self.ls)

        # And so on for every member of the ls.SUPPORTED_DIAGNOSTICS_TYPES list. 
        


