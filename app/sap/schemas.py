from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class CardType(str, Enum):
    CLIENT = "C"
    SUPPLIER = "S"


class AddressType(str, Enum):
    BILLING = "bo_BillTo"
    SHIPPING = "bo_ShipTo"


class BPAddress(BaseModel):
    AddressName: str
    Street: str
    Block: Optional[str] = None
    ZipCode: str
    City: str
    County: str
    Country: str = "BR"
    State: str
    BuildingFloorRoom: Optional[str] = None
    AddressType: AddressType
    TypeOfAddress: str
    StreetNo: str


class BPFiscalTaxID(BaseModel):
    Address: str = ""
    TaxId0: Optional[str] = None  # CNPJ
    TaxId4: Optional[str] = None  # CPF


class BusinessPartnerCreate(BaseModel):
    CardName: str
    CardType: CardType
    GroupCode: int
    CardForeignName: str
    AliasName: str
    Phone1: str  # DDD
    Phone2: str  # Telefone
    EmailAddress: str
    Series: str
    BPAddresses: List[BPAddress]
    BPFiscalTaxIDCollection: Optional[List[BPFiscalTaxID]] = None


class BusinessPartnerResponse(BaseModel):
    CardCode: str
    CardName: str
    CardType: str
