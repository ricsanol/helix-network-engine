from __future__ import annotations

import json
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

from helix.models.precheck_result import PreCheckResult


def _sanitize_filename(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]", "_", value)


def save_precheck_report(result: PreCheckResult, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)

    hostname = _sanitize_filename(result.hostname)
    vendor = _sanitize_filename(result.vendor.lower())

    output_file = reports_dir / f"{hostname}_{vendor}_precheck.json"

    # Escrita atômica (evita arquivo corrompido)
    with NamedTemporaryFile("w", delete=False, dir=reports_dir, encoding="utf-8") as tmp:
        json.dump(
            result.to_dict(),
            tmp,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )
        temp_path = Path(tmp.name)

    temp_path.replace(output_file)

    return output_file