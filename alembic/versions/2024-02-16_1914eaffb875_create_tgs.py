"""create tgs

Revision ID: 1914eaffb875
Revises: e6ad0215395d
Create Date: 2024-02-16 12:01:07.361816

"""

import sqlalchemy as sa
from alembic import op

revision = "1914eaffb875"
down_revision = "e6ad0215395d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tgs",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("tg", sa.BIGINT(), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("tgs")
