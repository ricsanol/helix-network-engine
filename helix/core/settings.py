from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


@dataclass(frozen=True)
class Settings:
    ssh_username: str
    ssh_password: str
    ssh_port: int
    ssh_timeout: int
    ssh_conn_timeout: int

    output_dir: Path
    reports_dir: Path
    logs_dir: Path
    approved_dir: Path
    blocked_dir: Path

    log_level: str

    @staticmethod
    def from_env() -> "Settings":
        base_output = Path(os.getenv("HELIX_OUTPUT_DIR", "outputs")).resolve()

        ssh_username = os.getenv("HELIX_SSH_USERNAME", "").strip()
        ssh_password = os.getenv("HELIX_SSH_PASSWORD", "")
        log_level = os.getenv("HELIX_LOG_LEVEL", "INFO").upper().strip()

        if not ssh_username:
            raise ValueError("Variável obrigatória ausente: HELIX_SSH_USERNAME")

        if not ssh_password:
            raise ValueError("Variável obrigatória ausente: HELIX_SSH_PASSWORD")

        if log_level not in VALID_LOG_LEVELS:
            raise ValueError(
                f"HELIX_LOG_LEVEL inválido: {log_level}. "
                f"Valores aceitos: {', '.join(sorted(VALID_LOG_LEVELS))}"
            )

        return Settings(
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            ssh_port=int(os.getenv("HELIX_SSH_PORT", "22")),
            ssh_timeout=int(os.getenv("HELIX_SSH_TIMEOUT", "20")),
            ssh_conn_timeout=int(os.getenv("HELIX_SSH_CONN_TIMEOUT", "15")),
            output_dir=base_output,
            reports_dir=Path(
                os.getenv("HELIX_REPORTS_DIR", str(base_output / "reports"))
            ).resolve(),
            logs_dir=Path(
                os.getenv("HELIX_LOGS_DIR", str(base_output / "logs"))
            ).resolve(),
            approved_dir=Path(
                os.getenv("HELIX_APPROVED_DIR", str(base_output / "approved"))
            ).resolve(),
            blocked_dir=Path(
                os.getenv("HELIX_BLOCKED_DIR", str(base_output / "blocked"))
            ).resolve(),
            log_level=log_level,
        )

    def ensure_directories(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.approved_dir.mkdir(parents=True, exist_ok=True)
        self.blocked_dir.mkdir(parents=True, exist_ok=True)

    def get_output_target_dir(self, success: bool) -> Path:
        return self.approved_dir if success else self.blocked_dir


settings = Settings.from_env()