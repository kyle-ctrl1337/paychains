import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr


class MerchantRegister(BaseModel):
    email: EmailStr
    password: str
    company_name: str | None = None


class MerchantLogin(BaseModel):
    email: EmailStr
    password: str


class MerchantUpdate(BaseModel):
    company_name: str | None = None
    webhook_url: str | None = None
    auto_convert_to: str | None = None
    settlement_address: dict | None = None


class MerchantResponse(BaseModel):
    id: uuid.UUID
    email: str
    company_name: str | None
    webhook_url: str | None
    auto_convert_to: str
    settlement_address: dict
    plan: str
    is_active: bool
    is_admin: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MerchantWithKeys(MerchantResponse):
    api_key_live: str
    api_key_test: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    merchant: MerchantResponse


class APIKeyResponse(BaseModel):
    api_key_live: str
    api_key_test: str
    message: str = "Store these keys securely. They will not be shown again."
