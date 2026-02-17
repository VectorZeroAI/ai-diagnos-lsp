#!/usr/bin/env python
"""
The cross file analysis worker thread
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from pygls.workspace import TextDocument

from lsprotocol import types

from .chains.LLM.BasicOmniproviderLLM import BasicOmniproviderLLMFactory
from .chains.LLM.BasicGeminiLLM import BasicGeminiLlmFactory
from .chains.LLM.BasicGroqLLM import BasicGroqLLMFactory
from .chains.LLM.BasicOpenrouterLLM import OpenrouterLlmFactory

from utils.parser import get_cross_file_context


if TYPE_CHECKING:
    from ai_diagnos_lsp.AIDiagnosLSPClass import AIDiagnosLSP

def CrossFileAnalyserWorkerThread(ls: AIDiagnosLSP, file: TextDocument):
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

    prompt = 


