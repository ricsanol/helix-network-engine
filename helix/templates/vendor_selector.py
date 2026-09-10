from typing import Optional


def normalize_vendor(vendor: str) -> str:
    if not vendor:
        return ""
    return str(vendor).strip().lower()


def normalize_modelo(modelo: Optional[str]) -> str:
    if not modelo:
        return ""
    return str(modelo).strip().lower()


def get_template_and_builder(vendor: str, modelo: Optional[str] = None):
    vendor_norm = normalize_vendor(vendor)
    modelo_norm = normalize_modelo(modelo)

    if vendor_norm == "cisco":
        if "xr" in modelo_norm or "ios xr" in modelo_norm:
            return "cisco/mobile_service_iosxr.j2", "cisco"

        return "cisco/mobile_service_ios.j2", "cisco"

    if vendor_norm == "huawei":
        return "huawei/mobile_service_vrp.j2", "huawei"

    if vendor_norm == "juniper":
        raise ValueError(
            f"Template ainda não implementado para Juniper | modelo={modelo}"
        )

    if vendor_norm == "nokia":
        raise ValueError(
            f"Template ainda não implementado para Nokia | modelo={modelo}"
        )

    raise ValueError(f"Vendor/modelo não suportado: vendor={vendor}, modelo={modelo}")