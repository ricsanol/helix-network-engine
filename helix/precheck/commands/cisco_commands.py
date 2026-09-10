class CiscoCommands:
    @staticmethod
    def interface_exists(interface_name: str) -> str:
        return f"show ip interface brief | include {interface_name}"

    @staticmethod
    def subinterface_exists(subinterface_name: str) -> str:
        return f"show running-config | include ^interface {subinterface_name}"

    @staticmethod
    def vrf_exists(vrf_name: str) -> str:
        return f"show running-config | include ^ip vrf {vrf_name}"