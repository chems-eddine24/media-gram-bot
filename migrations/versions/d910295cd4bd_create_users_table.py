"""create users table

Revision ID: d910295cd4bd
Revises: 
Create Date: 2026-03-14 15:31:29.991795

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = 'd910295cd4bd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("telegram_id", sa.String(), unique=True, nullable=False),
        sa.Column("telegram_username", sa.String(), unique=True, nullable=True),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")