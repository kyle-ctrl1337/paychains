import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False
    )
    customer_email: Mapped[str | None] = mapped_column(String(255))
    customer_wallet: Mapped[str | None] = mapped_column(String(255))
    plan_name: Mapped[str] = mapped_column(String(255), nullable=False)
    amount_usd: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    interval: Mapped[str] = mapped_column(String(20), nullable=False)
    preferred_chain: Mapped[str | None] = mapped_column(String(20))
    preferred_token: Mapped[str | None] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="active")
    current_period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    current_period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    next_payment_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    merchant = relationship("Merchant", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")
