from pydantic import BaseModel, EmailStr
from typing import Optional


class TokenRequest(BaseModel):
    customer_id: str
    expires_in_days: Optional[int] = 365


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    customer_id: str


class CustomerProfile(BaseModel):
    """Schema conforme documentação MkPlace"""
    customerId: str
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None


class UpdateCustomerProfile(BaseModel):
    """Schema para atualização de perfil"""
    email: Optional[EmailStr] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone: Optional[str] = None
