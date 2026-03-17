"""Add xpub_key to merchants.

Revision ID: 002
Revises: 001
Create Date: 2026-03-17
"""

from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("merchants", sa.Column("xpub_key", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("merchants", "xpub_key")
