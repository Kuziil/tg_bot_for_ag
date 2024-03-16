"""new column for shifts

Revision ID: 11a53a0434d4
Revises: 0d15f56ad462
Create Date: 2024-03-11 13:20:29.249448

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "11a53a0434d4"
down_revision = "0d15f56ad462"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "shifts",
        sa.Column("start_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
    )
    op.add_column(
        "shifts",
        sa.Column("end_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_column("shifts", "end_at")
    op.drop_column("shifts", "start_at")
