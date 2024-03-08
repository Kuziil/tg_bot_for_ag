"""rename column tg_bot_id to tg_bot in agencies

Revision ID: 3b758212bc75
Revises: 04efc47a5177
Create Date: 2024-02-17 14:01:14.834600

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3b758212bc75"
down_revision = "04efc47a5177"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("agencies", sa.Column("tg_bot", sa.BIGINT(), nullable=False))
    op.drop_column("agencies", "tg_bot_id")


def downgrade():
    op.add_column(
        "agencies",
        sa.Column("tg_bot_id", sa.BIGINT(), autoincrement=False, nullable=False),
    )
    op.drop_column("agencies", "tg_bot")
