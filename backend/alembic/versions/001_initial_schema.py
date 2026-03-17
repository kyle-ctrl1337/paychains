"""Initial schema — all 6 core tables

Revision ID: 001
Revises: None
Create Date: 2026-03-17
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── merchants ──────────────────────────────────────────────────────
    op.create_table(
        "merchants",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("company_name", sa.String(255), nullable=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("api_key_live", sa.String(64), unique=True, nullable=False),
        sa.Column("api_key_test", sa.String(64), unique=True, nullable=False),
        sa.Column("webhook_url", sa.Text, nullable=True),
        sa.Column("webhook_secret", sa.String(64), nullable=False),
        sa.Column("auto_convert_to", sa.String(20), server_default="USDC", nullable=False),
        sa.Column("settlement_address", JSONB, server_default="{}", nullable=False),
        sa.Column("plan", sa.String(20), server_default="free", nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true"), nullable=False),
        sa.Column("is_admin", sa.Boolean, server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # ── payment_links ──────────────────────────────────────────────────
    op.create_table(
        "payment_links",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("merchant_id", UUID(as_uuid=True), sa.ForeignKey("merchants.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("amount_usd", sa.Numeric(18, 2), nullable=True),
        sa.Column("currency", sa.String(10), server_default="USD", nullable=False),
        sa.Column(
            "accepted_chains",
            ARRAY(sa.Text),
            server_default=sa.text("'{ethereum,polygon,bsc,solana,bitcoin}'"),
            nullable=False,
        ),
        sa.Column(
            "accepted_tokens",
            ARRAY(sa.Text),
            server_default=sa.text("'{ETH,MATIC,BNB,SOL,BTC,USDC,USDT}'"),
            nullable=False,
        ),
        sa.Column("redirect_url", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", JSONB, server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # ── subscriptions ──────────────────────────────────────────────────
    op.create_table(
        "subscriptions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("merchant_id", UUID(as_uuid=True), sa.ForeignKey("merchants.id"), nullable=False),
        sa.Column("customer_email", sa.String(255), nullable=True),
        sa.Column("customer_wallet", sa.String(255), nullable=True),
        sa.Column("plan_name", sa.String(255), nullable=False),
        sa.Column("amount_usd", sa.Numeric(18, 2), nullable=False),
        sa.Column("interval", sa.String(20), nullable=False),
        sa.Column("preferred_chain", sa.String(20), nullable=True),
        sa.Column("preferred_token", sa.String(20), nullable=True),
        sa.Column("status", sa.String(20), server_default="active", nullable=False),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("next_payment_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("retry_count", sa.Integer, server_default=sa.text("0"), nullable=False),
        sa.Column("max_retries", sa.Integer, server_default=sa.text("3"), nullable=False),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", JSONB, server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # ── payments ───────────────────────────────────────────────────────
    op.create_table(
        "payments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("merchant_id", UUID(as_uuid=True), sa.ForeignKey("merchants.id"), nullable=False),
        sa.Column("payment_link_id", UUID(as_uuid=True), sa.ForeignKey("payment_links.id"), nullable=True),
        sa.Column("subscription_id", UUID(as_uuid=True), sa.ForeignKey("subscriptions.id"), nullable=True),
        sa.Column("status", sa.String(20), server_default="pending", nullable=False),
        sa.Column("amount_usd", sa.Numeric(18, 2), nullable=False),
        sa.Column("amount_crypto", sa.Numeric(36, 18), nullable=True),
        sa.Column("token", sa.String(20), nullable=False),
        sa.Column("chain", sa.String(20), nullable=False),
        sa.Column("deposit_address", sa.String(255), nullable=False),
        sa.Column("from_address", sa.String(255), nullable=True),
        sa.Column("tx_hash", sa.String(255), nullable=True),
        sa.Column("confirmations", sa.Integer, server_default=sa.text("0"), nullable=False),
        sa.Column("required_confirmations", sa.Integer, nullable=False),
        sa.Column("fee_amount_usd", sa.Numeric(18, 4), nullable=True),
        sa.Column("fee_percentage", sa.Numeric(5, 4), server_default=sa.text("0.01"), nullable=False),
        sa.Column("conversion_tx_hash", sa.String(255), nullable=True),
        sa.Column("converted_amount", sa.Numeric(18, 6), nullable=True),
        sa.Column("converted_token", sa.String(20), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", JSONB, server_default="{}", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # indexes on payments
    op.create_index("ix_payments_merchant_id", "payments", ["merchant_id"])
    op.create_index("ix_payments_status", "payments", ["status"])
    op.create_index("ix_payments_payment_link_id", "payments", ["payment_link_id"])
    op.create_index("ix_payments_subscription_id", "payments", ["subscription_id"])

    # ── webhook_events ─────────────────────────────────────────────────
    op.create_table(
        "webhook_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("merchant_id", UUID(as_uuid=True), sa.ForeignKey("merchants.id"), nullable=False),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column("status", sa.String(20), server_default="pending", nullable=False),
        sa.Column("attempts", sa.Integer, server_default=sa.text("0"), nullable=False),
        sa.Column("max_attempts", sa.Integer, server_default=sa.text("5"), nullable=False),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_response_code", sa.Integer, nullable=True),
        sa.Column("last_error", sa.Text, nullable=True),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )

    # ── payouts ────────────────────────────────────────────────────────
    op.create_table(
        "payouts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("merchant_id", UUID(as_uuid=True), sa.ForeignKey("merchants.id"), nullable=False),
        sa.Column("amount", sa.Numeric(18, 6), nullable=False),
        sa.Column("token", sa.String(20), nullable=False),
        sa.Column("chain", sa.String(20), nullable=False),
        sa.Column("to_address", sa.String(255), nullable=False),
        sa.Column("tx_hash", sa.String(255), nullable=True),
        sa.Column("status", sa.String(20), server_default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("payouts")
    op.drop_table("webhook_events")
    op.drop_index("ix_payments_subscription_id", table_name="payments")
    op.drop_index("ix_payments_payment_link_id", table_name="payments")
    op.drop_index("ix_payments_status", table_name="payments")
    op.drop_index("ix_payments_merchant_id", table_name="payments")
    op.drop_table("payments")
    op.drop_table("subscriptions")
    op.drop_table("payment_links")
    op.drop_table("merchants")
