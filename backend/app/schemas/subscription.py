import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class SubscriptionCreate(BaseModel):
    customer_email: str | None = None
    customer_wallet: str | None = None
    plan_name: str
    amount_usd: Decimal
    interval: str  # weekly, monthly, quarterly, yearly
    preferred_chain: str | None = None
    preferred_token: str | None = None
    metadata: dict = {}


class SubscriptionUpdate(BaseModel):
    plan_name: str | None = None
    amount_usd: Decimal | None = None
    status: str | None = None  # paused, active
    preferred_chain: str | None = None
    preferred_token: str | None = None


class SubscriptionResponse(BaseModel):
    id: uuid.UUID
    merchant_id: uuid.UUID
    customer_email: str | None
    customer_wallet: str | None
    plan_name: str
    amount_usd: Decimal
    interval: str
    preferred_chain: str | None
    preferred_token: str | None
    status: str
    current_period_start: datetime
    current_period_end: datetime
    next_payment_at: datetime
    retry_count: int
    max_retries: int
    cancelled_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
