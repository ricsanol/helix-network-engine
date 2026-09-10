from helix.precheck.clients.base import BaseSSHClient


class HuaweiSSHClient(BaseSSHClient):
    @property
    def device_type(self) -> str:
        return "huawei"