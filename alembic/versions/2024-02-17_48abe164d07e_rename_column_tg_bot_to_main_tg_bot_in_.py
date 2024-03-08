"""rename column tg_bot to main_tg_bot in agencies

Revision ID: 48abe164d07e
Revises: 3b758212bc75
Create Date: 2024-02-17 19:11:09.875026

"""

import sqlalchemy as sa
from alembic import op

revision = "48abe164d07e"
down_revision = "3b758212bc75"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("agencies", sa.Column("main_tg_bot", sa.BIGINT(), nullable=False))
    op.drop_column("agencies", "tg_bot")


def downgrade():
    op.add_column(
        "agencies",
        sa.Column("tg_bot", sa.BIGINT(), autoincrement=False, nullable=False),
    )
    op.drop_column("agencies", "main_tg_bot")
