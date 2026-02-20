#!/usr/bin/env python
from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict
from pygls.workspace import TextDocument
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
import time
from lsprotocol import types
import logging
import os

from ai_diagnos_lsp.AnalysisSubsystem.analysers.CrossFileLogicAnalyser import CrossFileLogicAnalyser
from ai_diagnos_lsp.AnalysisSubsystem.analysers.BasicDiagnoseFunction import BasicDiagnoseFunctionWorker
from ai_diagnos_lsp.AnalysisSubsystem.analysers.CrossFileAnalyser import CrossFileAnalyserWorkerThread
from .analysers.BasicLogicAnalyser import BasicLogicAnalyserWorker
from .analysers.BasicStyleAnalyser import BasicStyleAnalyserWorker
from .analysers.CrossFileStyleAnalyser import CrossFileStyleAnalyserWorker

if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import LiteralSupportedAnalysisTypes
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

if os.getenv("AI_DIAGNOS_LOG") is not None:
    log = True
else:
    log = False




class AnalysisSubsystemConfig(TypedDict):
    write: list[LiteralSupportedAnalysisTypes]
    open: list[LiteralSupportedAnalysisTypes]
    change: list[LiteralSupportedAnalysisTypes]
    command: list[LiteralSupportedAnalysisTypes]
    max_threads: int



class AnalysisSubsystem:
    """
    The Analysis handling subsystem. 
    Is an abstraction layer between raw analysis worker threads and the lsp side callers. 
    The lsp side callers just submit the document and the event to this subsystem, wich handeles everything else. 
    
    Functionality includes:
        debounce time (Done)
        optional cancelation (Not yet implemented)
        status gathering (Done)
        max_file_size checks.  (Done)
        Capping the amount of threads.  (Done)

    Configuration for what analysises to run is the following:
        ["AnalysisSubsystem"][event] = ["analysis_types", "list"]

    Full exprected configuration schema is: 
        The expected configuration structure is:
            at ls.config["AnalysisSubsystem"] is a: 
                {
                    "write": ["list", "of", "analyses", "to", "run"],
                    "open": ["list", "of", "analyses", "to", "run"],
                    "change": ["list", "of", "analyses", "to", "run"],
                    "command": ["list", "of", "analyses", "to", "run"],
                    "max_threads": 4
                }

    """
    def __init__(self, ls: AIDiagnosLSP) -> None:
        try:
            self.ls = ls
            self.executor = ThreadPoolExecutor(max_workers=self.ls.config["AnalysisSubsystem"]["max_threads"])
            self.submited_analyses: dict[str, dict[str, Future[None]]] = {}
            self.last_analysed_at: dict[str, dict[str, float]] = {}

            for i in self.ls.SUPPORTED_DIAGNOSTIC_TYPES:
                self.submited_analyses[i] = {}

            for i in self.ls.SUPPORTED_DIAGNOSTIC_TYPES:
                self.last_analysed_at[i] = {}

            if log:
                logging.info(f" Analysis Subsystem: gotten the config {self.ls.config} ")
        except Exception as e:
            if log:
                logging.error(f"Error in the __init__ method in the Analysis subsystem ERROR = {e}")
            raise RuntimeError(f"Error in the __init__ method in the Analysis subsystem ERROR = {e}") from e

    def submit_document_for_analysis(self,
                                     doc: TextDocument | Path,
                                     event: Literal["write", "open", "change", "command"]
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
                    "change": ["list", "of", "analyses", "to", "run"],
                    "command":  ["list", "of", "analyses", "to", "run"],
                    ...
                }
        """
        try:
            if isinstance(doc, TextDocument):
                uri = doc.uri
                if len(doc.lines) > self.ls.config["max_file_size"]:
                    self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Filesize bigger then max file size defined at config"))
                    return
            else:
                uri = doc.as_uri()
                with doc.open() as f:
                    if len(f.readlines()) > self.ls.config.get("max_file_size"):
                        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Filesize bigger then max file size defined at config"))
                        return

            for i in self.last_analysed_at:
                uris = self.last_analysed_at[i]
                if uri not in uris:
                    self.last_analysed_at[i][uri] = 0

            
            try:
                if "Basic" in self.ls.config["AnalysisSubsystem"][event]:
                    if time.time() - self.last_analysed_at["Basic"][uri] > self.ls.config["debounce_ms"] / 1000:
                        self.submited_analyses["Basic"][uri] = self.executor.submit(BasicDiagnoseFunctionWorker, doc, self.ls)
                        self.last_analysed_at["Basic"][uri] = time.time()
                    else:
                        # TODO : Implement a configuration option for "at debounce do".
                        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Debounced the analysis !"))

                if "CrossFile" in self.ls.config["AnalysisSubsystem"][event]:
                    if time.time() - self.last_analysed_at["CrossFile"][uri] > self.ls.config["debounce_ms"] / 1000:
                        self.submited_analyses["CrossFile"][uri] = self.executor.submit(CrossFileAnalyserWorkerThread, self.ls, doc)
                        self.last_analysed_at["CrossFile"][uri] = time.time()
                    else:
                        # TODO : Implement a configuration option for "at debounce do".
                        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Debounced the analysis !"))

                if "BasicLogic" in self.ls.config["AnalysisSubsystem"][event]:
                    if time.time() - self.last_analysed_at["BasicLogic"][uri] > self.ls.config["debounce_ms"] / 1000:
                        self.submited_analyses["BasicLogic"][uri] = self.executor.submit(BasicLogicAnalyserWorker, doc, self.ls)
                        self.last_analysed_at["BasicLogic"][uri] = time.time()
                    else:
                        # TODO : Implement a configuration option for "at debounce do".
                        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Debounced the analysis !"))

                if "CrossFileLogic" in self.ls.config["AnalysisSubsystem"][event]:
                    if time.time() - self.last_analysed_at["CrossFileLogic"][uri] > self.ls.config["debounce_ms"] / 1000:
                        self.submited_analyses["CrossFileLogic"][uri] = self.executor.submit(CrossFileLogicAnalyser, self.ls, doc)
                        self.last_analysed_at["CrossFileLogic"][uri] = time.time()
                    else:
                        # TODO : Implement a configuration option for "at debounce do".
                        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Debounced the analysis !"))

                if "CrossFileStyle" in self.ls.config["AnalysisSubsystem"][event]:
                    if time.time() - self.last_analysed_at["CrossFileStyle"][uri] > self.ls.config["debounce_ms"] / 1000:
                        self.submited_analyses["CrossFileStyle"][uri] = self.executor.submit(CrossFileStyleAnalyserWorker, doc, self.ls)
                        self.last_analysed_at["CrossFileStyle"][uri] = time.time()
                    else:
                        # TODO : Implement a configuration option for "at debounce do".
                        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Debounced the analysis !"))

                if "BasicStyle" in self.ls.config["AnalysisSubsystem"][event]:
                    if time.time() - self.last_analysed_at["BasicStyle"][uri] > self.ls.config["debounce_ms"] / 1000:
                        self.submited_analyses["BasicStyle"][uri] = self.executor.submit(BasicStyleAnalyserWorker, doc, self.ls)
                        self.last_analysed_at["BasicStyle"][uri] = time.time()
                    else:
                        # TODO : Implement a configuration option for "at debounce do".
                        self.ls.window_show_message(types.ShowMessageParams(types.MessageType(2), "Debounced the analysis !"))

            except KeyError as e:
                if log:
                    logging.error(f"Encountered a key error inside the config. {e}")
                raise RuntimeError(f"Encountered a key error inside the config. {e}") from e

            # And so on for every member of the ls.SUPPORTED_DIAGNOSTICS_TYPES list. 
        except Exception as e:
            raise RuntimeError(f"Otherwise uncaught exception happened in Analysis Subsystem Class file in submit document for analyis method. {e}") from e

    def get_status(self):
        """
    Status summary of the analysis subsystem, for the AI status command to grab
        """
        message = "AI diagnos status:"
        for i in self.ls.SUPPORTED_DIAGNOSTIC_TYPES:
            for j in self.submited_analyses[i].items():
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
        

def AnalysisSubsystemClassFactory(ls: AIDiagnosLSP):
    return AnalysisSubsystem(
            ls=ls
            )

