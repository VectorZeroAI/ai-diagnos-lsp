#!/usr/bin/env python3
from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.prompts.SHARED import TASK, NOTE, CONSISTENCY_ERROR_DESC, FOOTER, FORMAT_DESC, LOGIC_ERRORS_DESC
from ai_diagnos_lsp.AnalysisSubsystem.analysers.chains.PromptObjekts.prompts.EXEMPLARS import BAD_EXAMPLES, COT_EXAMPLES, GOOD_EXAMPLES

if TYPE_CHECKING:
    from ai_diagnos_lsp.default_config import user_config

def get_overrides(config: user_config, filetype: str) -> dict[str, str]:
    overrides = importlib.import_module(config['prompt_overrides'].get(filetype))

    ovrd = {
            "TASK": getattr(overrides, "TASK", TASK),
            "NOTE": getattr(overrides, "NOTE", NOTE),
            "LOGIC_ERRORS_DESC": getattr(overrides, "LOGIC_ERRORS_DESC", LOGIC_ERRORS_DESC),
            "CONSISTENCY_ERROR_DESC": getattr(overrides, "CONSISTENCY_ERROR_DESC", CONSISTENCY_ERROR_DESC),
            "FORMAT_DESC":  getattr(overrides, "FORMAT_DESC", FORMAT_DESC),
            "GOOD_EXAMPLES": getattr(overrides, "GOOD_EXAMPLES", GOOD_EXAMPLES),
            "COT_EXAMPLES": getattr(overrides, "COT_EXAMPLES", COT_EXAMPLES),
            "BAD_EXAMPLES": getattr(overrides, "BAD_EXAMPLES", BAD_EXAMPLES),
            "FOOTER": getattr(overrides, "FOOTER", FOOTER),
            }
    return ovrd
