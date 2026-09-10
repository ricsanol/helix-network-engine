from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class ValidationItem:
    name: str
    passed: bool
    severity: str = "ERROR"   # INFO | WARNING | ERROR
    message: str = ""
    details: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PreCheckResult:
    hostname: str
    vendor: str
    interface_name: str
    subinterface_name: Optional[str] = None
    vrf_name: Optional[str] = None
    success: bool = False
    executed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    items: List[ValidationItem] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def add_item(self, item: ValidationItem) -> None:
        self.items.append(item)

    def add_error(self, error_message: str) -> None:
        self.errors.append(error_message)

    def finalize(self) -> None:
        blocking_items = [item for item in self.items if item.severity.upper() == "ERROR"]
        self.success = all(item.passed for item in blocking_items) and not self.errors

    def to_dict(self) -> dict:
        return asdict(self)