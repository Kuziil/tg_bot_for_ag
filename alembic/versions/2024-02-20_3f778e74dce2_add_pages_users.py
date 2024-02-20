"""add pages_users

Revision ID: 3f778e74dce2
Revises: e06d40d15b1e
Create Date: 2024-02-20 11:57:34.437318

"""

from alembic import op
import sqlalchemy as sa


revision = "3f778e74dce2"
down_revision = "e06d40d15b1e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pages_users",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("page_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "page_id", name="idx_unique_page_users"),
    )


def downgrade():
    op.drop_table("pages_users")
