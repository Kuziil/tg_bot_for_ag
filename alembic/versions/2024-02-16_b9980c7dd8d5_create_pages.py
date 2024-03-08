"""create pages

Revision ID: b9980c7dd8d5
Revises: 1914eaffb875
Create Date: 2024-02-16 12:27:50.624909

"""

import sqlalchemy as sa
from alembic import op

revision = "b9980c7dd8d5"
down_revision = "1914eaffb875"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pages",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("vip", sa.BOOLEAN(), nullable=False),
        sa.Column("sales_commision", sa.NUMERIC(), nullable=False),
        sa.Column(
            "work_same_time", sa.BIGINT(), server_default=sa.text("1"), nullable=False
        ),
        sa.Column("page_link", sa.TEXT(), nullable=True),
        sa.Column("senior_id", sa.BIGINT(), nullable=True),
        sa.Column("model_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["senior_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("pages")
