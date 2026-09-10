from typing import List, Optional
from helix.models.cluster_model import ClusterModel


def normalize_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def find_cluster_by_hl3(hl3_hostname: str, clusters: List[ClusterModel]) -> Optional[ClusterModel]:
    target = normalize_text(hl3_hostname)

    for cluster in clusters:
        if normalize_text(cluster.hl3) == target:
            return cluster

    return None