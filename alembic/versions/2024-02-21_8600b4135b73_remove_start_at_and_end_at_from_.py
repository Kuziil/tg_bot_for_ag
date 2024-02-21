"""remove start_at and end_at from intervals

Revision ID: 8600b4135b73
Revises: 06772c1cb8f5
Create Date: 2024-02-21 17:44:43.168149

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "8600b4135b73"
down_revision = "06772c1cb8f5"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("intervals", "start_at")
    op.drop_column("intervals", "end_at")


def downgrade():
    op.add_column(
        "intervals",
        sa.Column(
            "end_at",
            postgresql.TIME(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "intervals",
        sa.Column(
            "start_at",
            postgresql.TIME(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
    )
