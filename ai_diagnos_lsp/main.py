#!/usr/bin/env python3

from typing import Sequence

from lsprotocol import types

import os
import logging

from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP
from .default_config import DEFAULT_CONFIG

def main():
    """
    The server setup and startup function. Also registeres the handlers.
    """
    server = AIDiagnosLSP('ai_diagnos', "v0.15 DEV")
    
    @server.feature(types.INITIALIZE)
    def on_startup(ls: AIDiagnosLSP, params: types.InitializeParams):
        """
        The configuration getting and saving function.
        pretty much sets the ls.config map

        and returns the capabilities of the server
        """

        ls.config = DEFAULT_CONFIG

        assert params.initialization_options is not None
        if os.getenv("AI_DIAGNOS_LOG"):
            logging.info(f"gotten the initialization options of {params.initialization_options}")
        for i in params.initialization_options:
            ls.config[i] = params.initialization_options.get(i)
            if os.getenv("AI_DIAGNOS_LOG"):
                logging.info(f"set parameter ls.config[{i}] to value {ls.config[i]}")


        return types.InitializeResult(
                capabilities=types.ServerCapabilities(
                    text_document_sync=types.TextDocumentSyncOptions(
                        open_close= True, will_save=True,
                        save=types.SaveOptions(include_text=True),
                        change=types.TextDocumentSyncKind.Full
                        ),
                    diagnostic_provider=types.DiagnosticOptions(
                        inter_file_dependencies=True,
                        workspace_diagnostics=True,
                        identifier="AI-diagnos-lsp"
                        )
                    )
                )



    @server.feature(types.INITIALIZED)
    def on_initialised(ls: AIDiagnosLSP, params: types.InitializedParams):
        """ Callback on initialisation completion """
        ls.init_subsystems()
        ls.DiagnosticsHandlingSubsystem.load_all_diagnostics()

    @server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
    def on_did_change(ls: AIDiagnosLSP, params: types.DidChangeTextDocumentParams):
        """ Publish diagnostics from DB to the client on change. e.g. refresh them. """

        ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(params.text_document.uri)

        doc = ls.workspace.get_text_document(params.text_document.uri)

        ls.AnalysisSubsystem.submit_document_for_analysis(doc, "change")

    @server.feature(types.TEXT_DOCUMENT_DID_OPEN)
    def did_open(ls: AIDiagnosLSP, params: types.DidOpenTextDocumentParams):
        """ Try to load saved diagnostics for the file, if fails, analyse.  """

        doc = ls.workspace.get_text_document(params.text_document.uri)

        if not ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(doc.uri):

            ls.AnalysisSubsystem.submit_document_for_analysis(doc, "open")

            ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(doc.uri)

    @server.feature(types.TEXT_DOCUMENT_DID_SAVE)
    def did_save(ls: AIDiagnosLSP, params: types.DidSaveTextDocumentParams):
        """ Diagnose each document when it is saved, e.g. on save. As was done by the previous version of the plugin """

        doc = ls.workspace.get_text_document(params.text_document.uri)

        ls.DiagnosticsHandlingSubsystem.register_file_write(doc.uri)

        ls.AnalysisSubsystem.submit_document_for_analysis(doc, "write")

        ls.DiagnosticsHandlingSubsystem.load_diagnostics_for_file(doc.uri)

    @server.feature(
            types.TEXT_DOCUMENT_DIAGNOSTIC,
            types.DiagnosticOptions(
                identifier="pull-diagnostics",
                inter_file_dependencies=True,
                workspace_diagnostics=True,
                ),
            )
    def document_diagnostic(ls: AIDiagnosLSP, params: types.DocumentDiagnosticParams):
        """ Return diagnostics for the requested document """
        
        if (uri := params.text_document.uri) not in ls.diagnostics:
            return

        version, diagnostics = ls.diagnostics[uri]
        result_id = f"{uri}@{version}"

        if result_id == params.previous_result_id:
            return types.UnchangedDocumentDiagnosticReport(result_id)

        return types.FullDocumentDiagnosticReport(items=diagnostics, result_id=result_id)

    @server.feature(types.WORKSPACE_DIAGNOSTIC)
    def workspace_diagnostic( ls: AIDiagnosLSP, params: types.WorkspaceDiagnosticParams ):
        """Return diagnostics for the workspace."""
        # logging.info("%s", params)
        items = []
        previous_ids = {result.value for result in params.previous_result_ids}

        for uri, (version, diagnostics) in ls.diagnostics.items():
            result_id = f"{uri}@{version}"
            if result_id in previous_ids:
                items.append(
                    types.WorkspaceUnchangedDocumentDiagnosticReport(
                        uri=uri, result_id=result_id, version=version
                    )
                )
            else:
                items.append(
                    types.WorkspaceFullDocumentDiagnosticReport(
                        uri=uri,
                        version=version,
                        items=diagnostics,
                    )
                )

        return types.WorkspaceDiagnosticReport(items=items)

    @server.command("Analyse.Document")
    def AnalyseDocument(ls: AIDiagnosLSP, params: Sequence[str]):
        """
        Analyses a document by URI . REQUIRES a URI as its parameter 
        
        With what analysers it analyses is decided by the configuration at the event command of the Analysis Subsystem
        """

        assert params is not None

        uri = "".join(params)
        doc = ls.workspace.get_text_document(uri)
        ls.AnalysisSubsystem.submit_document_for_analysis(doc, "command")
    
    @server.command("Clear.AIDiagnostics")
    def ClearAIDiagnostics(ls: AIDiagnosLSP, params: Sequence[str]):
        """
        Clears AI diagnostics for the provided URI.

        Non persistent, doesnt delete them from the DB. 
        To delete from the database, please delete the database. 
        In the future, delete will be added. 

        NOTE: Due to Neovim poorly supporting pull diagnostics, I just push the empty diagnostics. 
        """
        assert params is not None

        uri = "".join(params)
        ls.diagnostics[uri] = (-1, [])
        ls.text_document_publish_diagnostics(types.PublishDiagnosticsParams(uri=uri, diagnostics=[]))
        ls.window_show_message(types.ShowMessageParams(types.MessageType(3), "successfully cleared the diagnostics"))
        ls.workspace_diagnostic_refresh(None)

    @server.command("Clear.AIDiagnostics.All")
    def ClearAllAIDiagnostics(ls: AIDiagnosLSP):
        """
        Clears ALL the AI diagnostics 
        The same as with clear diagnostics. 
        """

        for i in ls.diagnostics:
            ls.diagnostics[i] = (-1, [])
            ls.text_document_publish_diagnostics(types.PublishDiagnosticsParams( uri=i, diagnostics=[]))
        ls.window_show_message(types.ShowMessageParams(types.MessageType(3), "succesfully cleared all the diagnostics"))
        ls.workspace_diagnostic_refresh(None)

    server.start_io()

if __name__ == "__main__":
    main()
