from __future__ import annotations

from abc import ABC, abstractmethod
from helix.models.precheck_result import PreCheckResult


class BasePreCheckValidator(ABC):
    @abstractmethod
    def run(
        self,
        hostname: str,
        vendor: str,
        interface_name: str,
        subinterface_name: str,
        vrf_name: str,
    ) -> PreCheckResult:
        raise NotImplementedError