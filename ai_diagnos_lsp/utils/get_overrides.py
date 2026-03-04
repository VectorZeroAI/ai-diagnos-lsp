#!/usr/bin/env python3
from __future__ import annotations

import sys
from importlib import util
from typing import TYPE_CHECKING

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.prompts.EXEMPLARS import (
    BAD_EXAMPLES,
    COT_EXAMPLES,
    GOOD_EXAMPLES,
)
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.prompts.SHARED import (
    CONSISTENCY_ERROR_DESC,
    CROSS_FILE_NOTE,
    FOOTER,
    FORMAT_DESC,
    LOGIC_ERRORS_DESC,
    NOTE,
    TASK,
)

if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import user_config


defaults = {
        "TASK": TASK,
        "NOTE": NOTE,
        "CROSS_FILE_NOTE": CROSS_FILE_NOTE,
        "LOGIC_ERRORS_DESC":LOGIC_ERRORS_DESC,
        "CONSISTENCY_ERROR_DESC": CONSISTENCY_ERROR_DESC,
        "FORMAT_DESC": FORMAT_DESC,
        "GOOD_EXAMPLES":GOOD_EXAMPLES,
        "COT_EXAMPLES":COT_EXAMPLES,
        "BAD_EXAMPLES":BAD_EXAMPLES,
        "FOOTER":FOOTER,
        }

def get_overrides(config: user_config, filetype: str) -> dict[str, str]:
    """
    The function that gets the overrides for the configuration and filetype. 
    If no overrides were found, RETURNS DEFAULTS.
    THE DEFAULTING LOGIC HAPPENDS HERE.
    """
    if config['prompt_overrides'].get(filetype) is not None:
        overrides_path = config['prompt_overrides'].get(filetype)
        spec = util.spec_from_file_location(f"_prompt_override_{filetype.lstrip('.')}", overrides_path)
        if spec is None or spec.loader is None:
            return defaults
        module = util.module_from_spec(spec)
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            return defaults

        ovrd = {
            "TASK": getattr(module, "TASK", TASK),
            "NOTE": getattr(module, "NOTE", NOTE),
            "CROSS_FILE_NOTE": getattr(module, "CROSS_FILE_NOTE", CROSS_FILE_NOTE),
            "LOGIC_ERRORS_DESC": getattr(module, "LOGIC_ERRORS_DESC", LOGIC_ERRORS_DESC),
            "CONSISTENCY_ERROR_DESC": getattr(module, "CONSISTENCY_ERROR_DESC", CONSISTENCY_ERROR_DESC),
            "FORMAT_DESC":  getattr(module, "FORMAT_DESC", FORMAT_DESC),
            "GOOD_EXAMPLES": getattr(module, "GOOD_EXAMPLES", GOOD_EXAMPLES),
            "COT_EXAMPLES": getattr(module, "COT_EXAMPLES", COT_EXAMPLES),
            "BAD_EXAMPLES": getattr(module, "BAD_EXAMPLES", BAD_EXAMPLES),
            "FOOTER": getattr(module, "FOOTER", FOOTER),
            }
    else:
        return defaults
    return ovrd
