"""create agencies

Revision ID: fc248bc57da4
Revises:
Create Date: 2024-02-16 07:12:00.181707

"""

from alembic import op
import sqlalchemy as sa


revision = "fc248bc57da4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agencies",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.Column("tg_bot_id", sa.BIGINT(), nullable=False),
        sa.Column("test_tg_bot", sa.BIGINT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("agencies")
