"""replace type for intervals time to datetime

Revision ID: d2cb9f9799ce
Revises: 8600b4135b73
Create Date: 2024-02-21 17:45:35.053071

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "d2cb9f9799ce"
down_revision = "8600b4135b73"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "intervals",
        sa.Column("start_at", postgresql.TIMESTAMP(timezone=True), nullable=False),
    )
    op.add_column(
        "intervals",
        sa.Column("end_at", postgresql.TIMESTAMP(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_column("intervals", "end_at")
    op.drop_column("intervals", "start_at")
