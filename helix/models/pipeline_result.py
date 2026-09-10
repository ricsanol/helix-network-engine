from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from helix.models.precheck_result import PreCheckResult


@dataclass
class PipelineResult:
    hostname: str
    vendor: str
    approved: bool
    decision_reason: str
    precheck_result: PreCheckResult

    rendered_config: Optional[str] = None
    script_path: Optional[Path] = None
    report_path: Optional[Path] = None

    def status_label(self) -> str:
        return "approved" if self.approved else "blocked"