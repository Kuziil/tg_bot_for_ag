"""rename tg to user_tg_id

Revision ID: 27b91351ecd9
Revises: 4ef0f4e2e8ea
Create Date: 2024-02-18 00:36:39.033612

"""

import sqlalchemy as sa
from alembic import op

revision = "27b91351ecd9"
down_revision = "4ef0f4e2e8ea"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tgs", sa.Column("user_tg_id", sa.BIGINT(), nullable=False))
    op.drop_column("tgs", "tg")


def downgrade():
    op.add_column(
        "tgs", sa.Column("tg", sa.BIGINT(), autoincrement=False, nullable=False)
    )
    op.drop_column("tgs", "user_tg_id")
