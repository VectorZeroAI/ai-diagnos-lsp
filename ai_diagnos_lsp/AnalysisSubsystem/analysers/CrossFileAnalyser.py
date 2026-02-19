#!/usr/bin/env python
"""
The cross file analysis worker thread
"""
from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

from pathlib import Path
import os
import logging

from pygls.workspace import TextDocument

from lsprotocol import types

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.GeneralDiagnosticsPydanticOutputParser import GeneralDiagnosticsOutputParserFactory
from ai_diagnos_lsp.utils.analyser.chain_invoker import chain_invoker_function

from .chains.LLM.BasicOmniproviderLLM import BasicOmniproviderLLMFactory
from .chains.LLM.BasicGeminiLLM import BasicGeminiLlmFactory
from .chains.LLM.BasicGroqLLM import BasicGroqLLMFactory
from .chains.LLM.BasicOpenrouterLLM import OpenrouterLlmFactory
from .chains.PromptObjekts.CrossFileAnalysisPrompt import CrossFileAnalysisPromptFactory



if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

if os.getenv("AI_DIAGNOS_LOG") is not None:
    LOG = True
else:
    LOG = False # # pyright: ignore

class CrossFileAnalysisConfig(TypedDict):
    scope: list[str]
    max_analysis_depth: int | None
    max_string_size_char: int | None


def CrossFileAnalyserWorkerThread(ls: AIDiagnosLSP, file: TextDocument | Path):
    """
    The worker thread

    Architecture:
        1. build the chain out of prompt + LLM + parser (according to LSP configuration)
        2. Invoke it in a thread with timeout as well as an optional pinger thread that notifies that 
            its still running
        3. register the results to the Diagnostics handling subsystem 
        4. Notify diagnostics handling subsystem to reload diagnostics for the file. 

    NOTE: DONT FORGET TO ENCAPSULATE EVERY DICTIONARY KEY ACCESS WITH TRY EXEPT KEY ERROR,
        and raise it back up with proper info of what and where caused it
    """
    
    try:

        if LOG:
            logging.info("Cross File analyser Worker thread started")
        try:
            if ls.config["use_omniprovider"]:

                llm = BasicOmniproviderLLMFactory(
                        model_openrouter=ls.config["model_openrouter"],
                        api_key_openrouter=ls.config["api_key_openrouter"],
                        api_key_gemini=ls.config["api_key_gemini"],
                        model_gemini=ls.config["model_gemini"],
                        fallback_models_gemini=ls.config.get("fallback_models_gemini"),
                        api_key_groq=ls.config["api_key_groq"],
                        model_groq=ls.config["model_groq"],
                        fallback_models_groq=ls.config.get("fallback_models_groq")
                        )

            elif ls.config["use_gemini"]:

                llm = BasicGeminiLlmFactory(
                        api_key_gemini=ls.config["api_key_gemini"],
                        model_gemini=ls.config["model_gemini"],
                        fallback_gemini_models=ls.config.get("fallback_models_gemini")
                        )

            elif ls.config["use_openrouter"]:
                llm = OpenrouterLlmFactory(
                        model_openrouter=ls.config["model_openrouter"],
                        api_key_openrouter=ls.config["api_key_openrouter"]
                        )

            elif ls.config['use_groq']:
                llm = BasicGroqLLMFactory(
                        model_groq=ls.config['model_groq'],
                        api_key_groq=ls.config['api_key_groq'],
                        fallback_models_groq=ls.config['fallback_models_groq']
                        )
            else:
                ls.window_show_message(types.ShowMessageParams(types.MessageType(1), "INVALID CONFIGURATION RECIEVED. One of use parameters must be true !"))
                raise RuntimeError("INVALID CONFIGURATION RECEIVED. One of use parameters must be true !")


        except KeyError as e:
            raise RuntimeError(f"lines 49-86, Cross file analyser thread, Key error {e}") from e

        prompt = CrossFileAnalysisPromptFactory()

        output_parser = GeneralDiagnosticsOutputParserFactory()

        chain = prompt | llm | output_parser

        chain_invoker_function(
                document=file,
                config=ls.config,
                chain=chain,
                ls=ls
                )
        
    except (KeyError, RuntimeError, Exception) as e:
        if isinstance(e, KeyError):
            raise RuntimeError(f"Unexpected key error in Cross file analyser thread. {e}") from e
        elif isinstance(e, RuntimeError):
            raise RuntimeError(f"Cross file analyser: possibly expected runtime-error {e}") from e
        else:
            raise RuntimeError(f"Unexpectec arbitrary exception occured in Cross file analyser thread. {e}") from e

