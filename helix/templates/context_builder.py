from ipaddress import ip_interface

from helix.models.mobile_service import MobileServiceModel
from helix.models.cluster_model import ClusterModel


def split_ip_and_mask(cidr_value: str):
    if not cidr_value:
        return None, None

    iface = ip_interface(cidr_value)
    return str(iface.ip), str(iface.network.netmask)


def build_cisco_context(service: MobileServiceModel, cluster: ClusterModel) -> dict:
    ip_mgmt, mask_mgmt = split_ip_and_mask(service.mobile_mgmt.gateway)
    ip_control, mask_control = split_ip_and_mask(service.mobile_control.gateway)
    ip_data, mask_data = split_ip_and_mask(service.mobile_data.gateway)

    return {
        "physical_interface": service.interface_serv,
        "description_base": service.id_sigla,

        "vrf_mgmt": cluster.mobile_access_mgmt,
        "vrf_control": cluster.mobile_control,
        "vrf_data": cluster.mobile_data,

        "ip_mgmt": ip_mgmt,
        "mask_mgmt": mask_mgmt,

        "ip_control": ip_control,
        "mask_control": mask_control,

        "ip_data": ip_data,
        "mask_data": mask_data,

        "vlan_mgmt": service.mobile_mgmt.vlan,
        "vlan_control": service.mobile_control.vlan,
        "vlan_data": service.mobile_data.vlan,

        "dhcp_1": cluster.dhcp_1,
        "dhcp_2": cluster.dhcp_2,
        "dhcp_3": cluster.dhcp_3,

        "hostname": service.hostname,
        "vendor": service.vendor,
        "modelo": service.modelo,
        "rr1": service.rr1,
    }


def build_huawei_context(service: MobileServiceModel, cluster: ClusterModel) -> dict:
    ip_mgmt, mask_mgmt = split_ip_and_mask(service.mobile_mgmt.gateway)
    ip_control, mask_control = split_ip_and_mask(service.mobile_control.gateway)
    ip_data, mask_data = split_ip_and_mask(service.mobile_data.gateway)

    return {
        "physical_interface": service.interface_serv,
        "description_base": service.id_sigla,

        "vrf_mgmt": cluster.mobile_access_mgmt,
        "vrf_control": cluster.mobile_control,
        "vrf_data": cluster.mobile_data,

        "ip_mgmt": ip_mgmt,
        "mask_mgmt": mask_mgmt,

        "ip_control": ip_control,
        "mask_control": mask_control,

        "ip_data": ip_data,
        "mask_data": mask_data,

        "vlan_mgmt": service.mobile_mgmt.vlan,
        "vlan_control": service.mobile_control.vlan,
        "vlan_data": service.mobile_data.vlan,

        "dhcp_1": cluster.dhcp_1,
        "dhcp_2": cluster.dhcp_2,
        "dhcp_3": cluster.dhcp_3,

        "hostname": service.hostname,
        "vendor": service.vendor,
        "modelo": service.modelo,
        "rr1": service.rr1,
    }