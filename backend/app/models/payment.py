import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False
    )
    payment_link_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("payment_links.id")
    )
    subscription_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subscriptions.id")
    )
    status: Mapped[str] = mapped_column(String(20), default="pending")
    amount_usd: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    amount_crypto: Mapped[Decimal | None] = mapped_column(Numeric(36, 18))
    token: Mapped[str] = mapped_column(String(20), nullable=False)
    chain: Mapped[str] = mapped_column(String(20), nullable=False)
    deposit_address: Mapped[str] = mapped_column(String(255), nullable=False)
    from_address: Mapped[str | None] = mapped_column(String(255))
    tx_hash: Mapped[str | None] = mapped_column(String(255))
    confirmations: Mapped[int] = mapped_column(Integer, default=0)
    required_confirmations: Mapped[int] = mapped_column(Integer, nullable=False)
    fee_amount_usd: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    fee_percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 4), default=Decimal("0.01")
    )
    conversion_tx_hash: Mapped[str | None] = mapped_column(String(255))
    converted_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    converted_token: Mapped[str | None] = mapped_column(String(20))
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    merchant = relationship("Merchant", back_populates="payments")
    payment_link = relationship("PaymentLink", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")
