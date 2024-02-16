"""create pages intervals

Revision ID: 847112d844ef
Revises: ad00ab25b81a
Create Date: 2024-02-16 18:14:41.223688

"""

from alembic import op
import sqlalchemy as sa


revision = "847112d844ef"
down_revision = "ad00ab25b81a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pages_intervals",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("page_id", sa.BIGINT(), nullable=False),
        sa.Column("interval_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["interval_id"], ["intervals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("page_id", "interval_id", name="idx_unique_page_interval"),
    )


def downgrade():
    op.drop_table("pages_intervals")
