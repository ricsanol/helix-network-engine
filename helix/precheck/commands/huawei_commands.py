class HuaweiCommands:
    @staticmethod
    def interface_exists(interface_name: str) -> str:
        return f"display interface {interface_name}"

    @staticmethod
    def subinterface_exists(subinterface_name: str) -> str:
        return f"display current-configuration interface {subinterface_name}"

    @staticmethod
    def vrf_exists(vrf_name: str) -> str:
        return f"display current-configuration | include ip vpn-instance {vrf_name}"