from typing import Optional, List
from pydantic import BaseModel, Field


# Request Models
class MerchantAddress(BaseModel):
    street: str
    number: str
    complement: Optional[str] = None
    neighborhood: str
    city: str
    state: str
    zip_code: str = Field(alias="zipCode")


class MerchantBankAccount(BaseModel):
    bank_code: str = Field(alias="bankCode")
    branch: str
    account: str
    account_digit: str = Field(alias="accountDigit")
    account_type: str = Field(alias="accountType")  # checking, savings


class MerchantContact(BaseModel):
    name: str
    email: str
    phone: str


class MerchantCompany(BaseModel):
    legal_name: str = Field(alias="legalName")
    trade_name: str = Field(alias="tradeName")
    document: str  # CNPJ
    mcc: str  # Merchant Category Code


class CreateMerchantRequest(BaseModel):
    company: MerchantCompany
    address: MerchantAddress
    bank_account: MerchantBankAccount = Field(alias="bankAccount")
    contacts: List[MerchantContact]


# Response Models
class MerchantResponse(BaseModel):
    _code: str = Field(alias="Code")
    status: str
    company: Optional[MerchantCompany] = None
    address: Optional[MerchantAddress] = None
    bank_account: Optional[MerchantBankAccount] = None
    contacts: Optional[List[MerchantContact]] = None


class ListMerchantsResponse(BaseModel):
    merchants: List[MerchantResponse]
    total: int
    page: int
    page_size: int = Field(alias="pageSize")
