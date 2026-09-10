from helix.precheck.clients.cisco_client import CiscoSSHClient
from helix.precheck.clients.huawei_client import HuaweiSSHClient
from helix.precheck.exceptions import UnsupportedVendorError
from helix.precheck.validators.cisco_validator import CiscoPreCheckValidator
from helix.precheck.validators.huawei_validator import HuaweiPreCheckValidator


def detect_cisco_platform(modelo: str) -> str:
    modelo_normalized = (modelo or "").strip().lower()

    if "xr" in modelo_normalized or "ios xr" in modelo_normalized:
        return "cisco_xr"

    return "cisco_ios"


def detect_huawei_platform(modelo: str) -> str:
    return "huawei_vrp"


def detect_juniper_platform(modelo: str) -> str:
    return "juniper_junos"


def detect_nokia_platform(modelo: str) -> str:
    return "nokia_sros"

from typing import Optional

def detect_platform(vendor: str, modelo: Optional[str] = None) -> str:
    vendor_normalized = (vendor or "").strip().lower()
    modelo_normalized = (modelo or "").strip()

    if vendor_normalized == "cisco":
        return detect_cisco_platform(modelo_normalized)

    if vendor_normalized == "huawei":
        return detect_huawei_platform(modelo_normalized)

    if vendor_normalized == "juniper":
        return detect_juniper_platform(modelo_normalized)

    if vendor_normalized == "nokia":
        return detect_nokia_platform(modelo_normalized)

    raise UnsupportedVendorError(
        f"Vendor não suportado para pre-check: vendor={vendor}, modelo={modelo}"
    )


def create_precheck_components(
    vendor: str,
    modelo: Optional[str],
    host: str,
    username: str,
    password: str,
    port: int = 22,
    timeout: int = 20,
    conn_timeout: int = 15,
):
    platform = detect_platform(vendor=vendor, modelo=modelo)

    if platform in ("cisco_ios", "cisco_xr"):
        client = CiscoSSHClient(
            host=host,
            username=username,
            password=password,
            port=port,
            timeout=timeout,
            conn_timeout=conn_timeout,
            platform=platform,
        )
        validator = CiscoPreCheckValidator(client)

    elif platform == "huawei_vrp":
        client = HuaweiSSHClient(
            host=host,
            username=username,
            password=password,
            port=port,
            timeout=timeout,
            conn_timeout=conn_timeout,
        )
        validator = HuaweiPreCheckValidator(client)

    elif platform == "juniper_junos":
        raise UnsupportedVendorError(
            f"Pre-check ainda não implementado para Juniper | modelo={modelo}"
        )

    elif platform == "nokia_sros":
        raise UnsupportedVendorError(
            f"Pre-check ainda não implementado para Nokia | modelo={modelo}"
        )

    else:
        raise UnsupportedVendorError(
            f"Plataforma não suportada para pre-check: {platform}"
        )

    return client, validator