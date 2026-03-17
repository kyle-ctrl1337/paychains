import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PaymentLink(Base):
    __tablename__ = "payment_links"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    merchant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("merchants.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    amount_usd: Mapped[Decimal | None] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    accepted_chains: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=lambda: ["ethereum", "polygon", "bsc", "solana", "bitcoin"],
    )
    accepted_tokens: Mapped[list[str]] = mapped_column(
        ARRAY(Text),
        default=lambda: ["ETH", "MATIC", "BNB", "SOL", "BTC", "USDC", "USDT"],
    )
    redirect_url: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    merchant = relationship("Merchant", back_populates="payment_links")
    payments = relationship("Payment", back_populates="payment_link")
