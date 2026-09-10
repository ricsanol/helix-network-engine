from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

from helix.precheck.exceptions import CommandExecutionError, SSHConnectionError


class BaseSSHClient(ABC):
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        port: int = 22,
        timeout: int = 20,
        conn_timeout: int = 15,
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.conn_timeout = conn_timeout
        self.connection: Optional[Any] = None

    @property
    @abstractmethod
    def device_type(self) -> str:
        raise NotImplementedError

    def connect(self) -> None:
        try:
            self.connection = ConnectHandler(
                device_type=self.device_type,
                host=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                timeout=self.timeout,
                conn_timeout=self.conn_timeout,
                fast_cli=False,
            )
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as exc:
            raise SSHConnectionError(
                f"Falha ao conectar no host {self.host}: {exc}"
            ) from exc
        except Exception as exc:
            raise SSHConnectionError(
                f"Erro inesperado na conexão com {self.host}: {exc}"
            ) from exc

    def disconnect(self) -> None:
        if not self.connection:
            return

        try:
            self.connection.disconnect()
        except Exception:
            pass
        finally:
            self.connection = None

    def is_connected(self) -> bool:
        return self.connection is not None

    def send_command(self, command: str) -> str:
        if not self.connection:
            raise CommandExecutionError("Conexão SSH não estabelecida.")

        try:
            output = self.connection.send_command(command, read_timeout=self.timeout)
            return output if output is not None else ""
        except Exception as exc:
            raise CommandExecutionError(
                f"Erro ao executar comando '{command}' em {self.host}: {exc}"
            ) from exc

    def __enter__(self) -> "BaseSSHClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()