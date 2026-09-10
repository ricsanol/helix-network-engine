from typing import Optional
from pydantic import BaseModel, Field


class ClusterModel(BaseModel):
    hl3: str = Field(..., alias="HL3")

    mobile_control: str = Field(..., alias="MOBILE-CONTROL")
    mobile_control_rd: str = Field(..., alias="MOBILE-CONTROL-RD")
    mobile_control_hrt_export: str = Field(..., alias="MOBILE-CONTROL-HRT-export")
    mobile_control_srt_import: str = Field(..., alias="MOBILE-CONTROL-SRT-import")

    mobile_data: str = Field(..., alias="MOBILE-DATA")
    mobile_data_rd: str = Field(..., alias="MOBILE-DATA-RD")
    mobile_data_hrt_export: str = Field(..., alias="MOBILE-DATA-HRT-export")
    mobile_data_srt_import: str = Field(..., alias="MOBILE-DATA-SRT-import")

    mobile_access_mgmt: str = Field(..., alias="MOBILE-ACCESS-MGMT")
    mobile_access_mgmt_rd: str = Field(..., alias="MOBILE-ACCESS-MGMT-RD")
    mobile_access_mgmt_srt_import: str = Field(..., alias="MOBILE-ACCESS-MGMT-SRT-import")
    mobile_access_mgmt_hrt_export: str = Field(..., alias="MOBILE-ACCESS-MGMT-HRT-export")

    dhcp_1: Optional[str] = Field(None, alias="DHCP 1")
    dhcp_2: Optional[str] = Field(None, alias="DHCP 2")
    dhcp_3: Optional[str] = Field(None, alias="DHCP 3")

    uf: Optional[str] = Field(None, alias="UF")
    rf_vendor: Optional[str] = Field(None, alias="RF VENDOR")