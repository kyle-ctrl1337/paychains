import uuid
from datetime import datetime
from pydantic import BaseModel


class WebhookEventResponse(BaseModel):
    id: uuid.UUID
    merchant_id: uuid.UUID
    event_type: str
    payload: dict
    status: str
    attempts: int
    max_attempts: int
    next_retry_at: datetime | None
    last_response_code: int | None
    last_error: str | None
    delivered_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class WebhookTestRequest(BaseModel):
    event_type: str = "payment.completed"


class PayoutRequest(BaseModel):
    amount: float
    token: str
    chain: str
    to_address: str


class PayoutResponse(BaseModel):
    id: uuid.UUID
    merchant_id: uuid.UUID
    amount: float
    token: str
    chain: str
    to_address: str
    tx_hash: str | None
    status: str
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class AnalyticsOverview(BaseModel):
    total_volume_usd: float
    total_transactions: int
    total_revenue_usd: float
    active_subscriptions: int
    period_start: datetime
    period_end: datetime


class ChainBreakdown(BaseModel):
    chain: str
    volume_usd: float
    transaction_count: int


class TokenBreakdown(BaseModel):
    token: str
    volume_usd: float
    transaction_count: int


class RevenueDataPoint(BaseModel):
    date: str
    revenue_usd: float
    transaction_count: int
