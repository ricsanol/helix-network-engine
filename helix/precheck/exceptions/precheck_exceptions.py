class PreCheckError(Exception):
    """Erro base do módulo de pre-check."""


class UnsupportedVendorError(PreCheckError):
    """Vendor não suportado para pre-check."""


class SSHConnectionError(PreCheckError):
    """Falha ao conectar via SSH no equipamento."""


class CommandExecutionError(PreCheckError):
    """Falha ao executar comando no equipamento."""


class ValidationExecutionError(PreCheckError):
    """Falha ao executar regra de validação."""