from helix.models.mobile_service import MobileServiceModel, MobileSegment


def _safe_int(value):
    try:
        if value is None or value == "":
            return None
        return int(value)
    except Exception:
        return None


def map_row_to_service(row: dict) -> MobileServiceModel:
    return MobileServiceModel(
        Hostname=row.get("Hostname"),
        Vendor=row.get("Vendor"),
        Modelo=row.get("Modelo"),
        **{"Loopback /32 IPV4": row.get("Loopback /32 IPV4")},
        RR1=row.get("RR1"),
        ID_SIGLA=row.get("ID_SIGLA"),
        **{"INTERFACE-SERV": row.get("INTERFACE-SERV")},

        mobile_data=MobileSegment(
            gateway=row.get("GATEWAY MOBILE-DATA"),
            baseband=row.get("BASEBAND MOBILE-DATA"),
            vlan=_safe_int(row.get("VLAN MOBILE-DATA")),
        ),

        mobile_control=MobileSegment(
            gateway=row.get("GATEWAY MOBILE-CONTROL"),
            baseband=row.get("BASEBAND MOBILE-CONTROL"),
            vlan=_safe_int(row.get("VLAN MOBILE-CONTROL")),
        ),

        mobile_mgmt=MobileSegment(
            gateway=row.get("GATEWAY MOBILE-MGMT"),
            baseband=row.get("BASEBAND MOBILE-MGMT"),
            vlan=_safe_int(row.get("VLAN MOBILE-MGMT")),
        ),
    )