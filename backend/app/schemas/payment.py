import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class PaymentLinkCreate(BaseModel):
    title: str
    description: str | None = None
    amount_usd: Decimal | None = None
    currency: str = "USD"
    accepted_chains: list[str] = ["ethereum", "polygon", "bsc", "solana", "bitcoin"]
    accepted_tokens: list[str] = ["ETH", "MATIC", "BNB", "SOL", "BTC", "USDC", "USDT"]
    redirect_url: str | None = None
    expires_at: datetime | None = None
    metadata: dict = {}


class PaymentLinkUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    amount_usd: Decimal | None = None
    accepted_chains: list[str] | None = None
    accepted_tokens: list[str] | None = None
    redirect_url: str | None = None
    is_active: bool | None = None


class PaymentLinkResponse(BaseModel):
    id: uuid.UUID
    merchant_id: uuid.UUID
    title: str
    description: str | None
    amount_usd: Decimal | None
    currency: str
    accepted_chains: list[str]
    accepted_tokens: list[str]
    redirect_url: str | None
    is_active: bool
    expires_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentCreate(BaseModel):
    amount_usd: Decimal
    token: str
    chain: str
    metadata: dict = {}
    payment_link_id: uuid.UUID | None = None


class PaymentResponse(BaseModel):
    id: uuid.UUID
    merchant_id: uuid.UUID
    payment_link_id: uuid.UUID | None
    subscription_id: uuid.UUID | None
    status: str
    amount_usd: Decimal
    amount_crypto: Decimal | None
    token: str
    chain: str
    deposit_address: str
    from_address: str | None
    tx_hash: str | None
    confirmations: int
    required_confirmations: int
    fee_amount_usd: Decimal | None
    fee_percentage: Decimal
    expires_at: datetime
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CheckoutInitiate(BaseModel):
    chain: str
    token: str
    customer_email: str | None = None


class CheckoutStatusResponse(BaseModel):
    payment_id: uuid.UUID
    status: str
    confirmations: int
    required_confirmations: int
    amount_usd: Decimal
    amount_crypto: Decimal | None
    token: str
    chain: str
    deposit_address: str
    expires_at: datetime


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    per_page: int
    pages: int
