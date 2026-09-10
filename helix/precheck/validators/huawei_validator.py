from __future__ import annotations

from helix.models.precheck_result import PreCheckResult, ValidationItem
from helix.precheck.commands.huawei_commands import HuaweiCommands
from helix.precheck.validators.base import BasePreCheckValidator


class HuaweiPreCheckValidator(BasePreCheckValidator):
    def __init__(self, client) -> None:
        self.client = client

    def run(
        self,
        hostname: str,
        vendor: str,
        interface_name: str,
        subinterface_name: str,
        vrf_name: str | None,
    ) -> PreCheckResult:
        result = PreCheckResult(
            hostname=hostname,
            vendor=vendor,
            interface_name=interface_name,
            subinterface_name=subinterface_name,
            vrf_name=vrf_name,
        )

        result.add_item(self._validate_physical_interface(interface_name))
        result.add_item(self._validate_subinterface_not_exists(subinterface_name))
        result.add_item(self._validate_vrf_exists(vrf_name))

        result.finalize()
        return result

    @staticmethod
    def _normalize_output(output: str) -> str:
        return (output or "").strip().lower()

    def _validate_physical_interface(self, interface_name: str) -> ValidationItem:
        output = self.client.send_command(HuaweiCommands.interface_exists(interface_name))
        normalized_output = self._normalize_output(output)
        normalized_interface = interface_name.strip().lower()

        interface_found = (
            "wrong parameter" not in normalized_output
            and "error:" not in normalized_output
            and "failed" not in normalized_output
            and normalized_interface in normalized_output
        )

        return ValidationItem(
            name="physical_interface_exists",
            passed=interface_found,
            severity="ERROR",
            message=(
                f"Interface física {interface_name} encontrada."
                if interface_found
                else f"Interface física {interface_name} não encontrada."
            ),
            details=output,
        )

    def _validate_subinterface_not_exists(self, subinterface_name: str) -> ValidationItem:
        output = self.client.send_command(
            HuaweiCommands.subinterface_exists(subinterface_name)
        )
        normalized_output = self._normalize_output(output)
        normalized_subinterface = subinterface_name.strip().lower()

        already_exists = (
            "wrong parameter" not in normalized_output
            and "error:" not in normalized_output
            and normalized_subinterface in normalized_output
        )

        return ValidationItem(
            name="subinterface_not_exists",
            passed=not already_exists,
            severity="ERROR",
            message=(
                f"Subinterface {subinterface_name} ainda não existe."
                if not already_exists
                else f"Subinterface {subinterface_name} já existe."
            ),
            details=output,
        )

    def _validate_vrf_exists(self, vrf_name: str | None) -> ValidationItem:
        if not vrf_name or not vrf_name.strip():
            return ValidationItem(
                name="vrf_exists",
                passed=False,
                severity="ERROR",
                message="VRF/VPN instance não informada para validação.",
                details=None,
            )

        output = self.client.send_command(HuaweiCommands.vrf_exists(vrf_name))
        normalized_output = self._normalize_output(output)
        normalized_vrf = vrf_name.strip().lower()

        exists = (
            "wrong parameter" not in normalized_output
            and "error:" not in normalized_output
            and normalized_vrf in normalized_output
        )

        return ValidationItem(
            name="vrf_exists",
            passed=exists,
            severity="ERROR",
            message=(
                f"VPN instance/VRF {vrf_name} encontrada."
                if exists
                else f"VPN instance/VRF {vrf_name} não encontrada."
            ),
            details=output,
        )