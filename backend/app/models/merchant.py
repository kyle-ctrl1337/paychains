import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key_live: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    api_key_test: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    webhook_url: Mapped[str | None] = mapped_column(Text)
    webhook_secret: Mapped[str] = mapped_column(String(64), nullable=False)
    auto_convert_to: Mapped[str] = mapped_column(String(20), default="USDC")
    settlement_address: Mapped[dict] = mapped_column(JSONB, default=dict)
    xpub_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    plan: Mapped[str] = mapped_column(String(20), default="free")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    payment_links = relationship("PaymentLink", back_populates="merchant")
    payments = relationship("Payment", back_populates="merchant")
    subscriptions = relationship("Subscription", back_populates="merchant")
    webhook_events = relationship("WebhookEvent", back_populates="merchant")
    payouts = relationship("Payout", back_populates="merchant")
