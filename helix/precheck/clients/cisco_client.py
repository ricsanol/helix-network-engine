from helix.precheck.clients.base import BaseSSHClient


class CiscoSSHClient(BaseSSHClient):
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 20,
        conn_timeout: int = 15,
        platform: str = "cisco_ios",  # 👈 NOVO
    ):
        super().__init__(
            host=host,
            username=username,
            password=password,
            port=port,
            timeout=timeout,
            conn_timeout=conn_timeout,
        )

        self.platform = platform

    @property
    def device_type(self) -> str:
        """
        Define o device_type do Netmiko baseado na plataforma.
        """

        if self.platform == "cisco_ios":
            return "cisco_ios"

        if self.platform == "cisco_xr":
            return "cisco_xr"

        # fallback seguro
        return "cisco_ios"