"""create shifts

Revision ID: 9c8334d7a0b4
Revises: 847112d844ef
Create Date: 2024-02-16 18:42:44.766126

"""

from alembic import op
import sqlalchemy as sa


revision = "9c8334d7a0b4"
down_revision = "847112d844ef"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "shifts",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("date_shift", sa.DATE(), nullable=False),
        sa.Column("page_interval_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["page_interval_id"], ["pages_intervals.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("shifts")
