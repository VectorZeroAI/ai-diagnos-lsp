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

        for i in self.ls.SUPPORTED_DIAGNOSTIC_TYPES:
            self.submited_analyses[i] = {}

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

        To understand what to submit, it looks up the configuration for that specifc event. 
        
        The expected configuration structure is:
            at ls.config["AnalysisSubsystem"] is a: 
                {
                    "write": ["list", "of", "analyses", "to", "run"],
                    "open": ["list", "of", "analyses", "to", "run"],
                    "change": ["list", "of", "analyses", "to", "run"]
                }
        """


        if type(doc) is TextDocument:
            uri = doc.uri
            if len(doc.lines) > self.ls.config["max_file_size"]:
                self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Filesize bigger then max file size defined at config"))
                return
        elif type(doc) is Path:
            uri = doc.as_uri()
            with doc.open() as f:
                if len(f.readlines()) > self.ls.config["max_file_size"]:
                    self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Filesize bigger then max file size defined at config"))
                    return
        else:
            raise TypeError(f"Invalid input type on doc parameter. Got {doc} of type {type(doc)}, expected object of type TextDocument or Path")
        
        if "Basic" in self.config[event]:
            if time.time() - self.last_analysed_at["Basic"][uri] < self.ls.config["debounce_ms"]:
                self.submited_analyses["Basic"][uri] = self.executor.submit(BasicDiagnoseFunctionWorker, doc, self.ls)
                self.last_analysed_at["Basic"][uri] = time.time()
            else:
                # TODO : Implement a configuration option for "at debounce do".
                # The options may be "ignore_new" , "cancell_old_and_start_new"
                self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Debounced the analysis !"))


        if "CrossFile" in self.config[event]:
            raise NotImplementedError("Cross file diagnostics not yet implemented")

        # And so on for every member of the ls.SUPPORTED_DIAGNOSTICS_TYPES list. 





    def get_status(self):
        """
    Status summary of the analysis subsystem, for the AI status command to grab
        """
        message = "AI diagnos status:"
        for i in self.ls.SUPPORTED_DIAGNOSTIC_TYPES:
            for j in self.submited_analyses[i].items:
                if j[1].done():
                    message = message + f"Analysis done for for file at {j[0]} \n"
                    message = message + f"    The analysis is of type {i} \n"
                elif j[1].cancelled():
                    message = message + f"Analysis cancelled for file at {j[0]} \n"
                    message = message + f"    The analysis is of type {i} \n"
                else:
                    message = message + f"Analysis still enquewed for file at {j[0]} \n"
                    message = message + f"    The analysis is of type {i} \n"

        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(3), message))
        


