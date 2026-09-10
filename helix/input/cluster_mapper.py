from helix.models.cluster_model import ClusterModel


def map_row_to_cluster(row: dict) -> ClusterModel:
    return ClusterModel(
        HL3=row.get("HL3"),
        **{"MOBILE-CONTROL": row.get("MOBILE-CONTROL")},
        **{"MOBILE-CONTROL-RD": row.get("MOBILE-CONTROL-RD")},
        **{"MOBILE-CONTROL-HRT-export": row.get("MOBILE-CONTROL-HRT-export")},
        **{"MOBILE-CONTROL-SRT-import": row.get("MOBILE-CONTROL-SRT-import")},

        **{"MOBILE-DATA": row.get("MOBILE-DATA")},
        **{"MOBILE-DATA-RD": row.get("MOBILE-DATA-RD")},
        **{"MOBILE-DATA-HRT-export": row.get("MOBILE-DATA-HRT-export")},
        **{"MOBILE-DATA-SRT-import": row.get("MOBILE-DATA-SRT-import")},

        **{"MOBILE-ACCESS-MGMT": row.get("MOBILE-ACCESS-MGMT")},
        **{"MOBILE-ACCESS-MGMT-RD": row.get("MOBILE-ACCESS-MGMT-RD")},
        **{"MOBILE-ACCESS-MGMT-SRT-import": row.get("MOBILE-ACCESS-MGMT-SRT-import")},
        **{"MOBILE-ACCESS-MGMT-HRT-export": row.get("MOBILE-ACCESS-MGMT-HRT-export")},

        **{"DHCP 1": row.get("DHCP 1")},
        **{"DHCP 2": row.get("DHCP 2")},
        **{"DHCP 3": row.get("DHCP 3")},
        UF=row.get("UF"),
        **{"RF VENDOR": row.get("RF VENDOR")},
    )