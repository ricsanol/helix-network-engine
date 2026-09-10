from typing import Optional
from pydantic import BaseModel, Field, field_validator


class MobileSegment(BaseModel):
    gateway: Optional[str] = None
    baseband: Optional[str] = None
    vlan: Optional[int] = None

    def is_configured(self) -> bool:
        return any([self.gateway, self.baseband, self.vlan])

    @field_validator("gateway", "baseband", mode="before")
    @classmethod
    def coerce_to_string(cls, v):
        if v is None or v == "":
            return None
        return str(v).strip()

    @field_validator("vlan", mode="before")
    @classmethod
    def coerce_vlan(cls, v):
        if v is None or v == "":
            return None
        return int(v)

    @field_validator("vlan")
    @classmethod
    def validate_vlan(cls, v):
        if v is not None and (v < 1 or v > 4094):
            raise ValueError("VLAN inválida")
        return v


class MobileServiceModel(BaseModel):
    hostname: str = Field(..., alias="Hostname")
    vendor: str = Field(..., alias="Vendor")
    modelo: Optional[str] = Field(None, alias="Modelo")
    loopback_ipv4: str = Field(..., alias="Loopback /32 IPV4")
    rr1: Optional[str] = Field(None, alias="RR1")
    id_sigla: str = Field(..., alias="ID_SIGLA")
    interface_serv: Optional[str] = Field(None, alias="INTERFACE-SERV")
    mobile_data: MobileSegment
    mobile_control: MobileSegment
    mobile_mgmt: MobileSegment

    @field_validator(
        "hostname",
        "vendor",
        "modelo",
        "loopback_ipv4",
        "id_sigla",
        "rr1",
        "interface_serv",
        mode="before",
    )
    @classmethod
    def normalize_string_fields(cls, v):
        if v is None or v == "":
            return None
        return str(v).strip()

    @field_validator("hostname", "vendor", "loopback_ipv4", "id_sigla")
    @classmethod
    def required_fields(cls, v):
        if not v or str(v).strip() == "":
            raise ValueError("Campo obrigatório vazio")
        return v

    @field_validator("interface_serv")
    @classmethod
    def validate_interface(cls, v):
        if not v or str(v).strip() == "":
            raise ValueError("INTERFACE-SERV não preenchida")
        return v