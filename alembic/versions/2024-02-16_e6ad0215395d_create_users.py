"""create users

Revision ID: e6ad0215395d
Revises: 5456b4bc00ae
Create Date: 2024-02-16 11:38:33.847450

"""

import sqlalchemy as sa
from alembic import op

revision = "e6ad0215395d"
down_revision = "5456b4bc00ae"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("username", sa.TEXT(), nullable=True),
        sa.Column("emoji", sa.TEXT(), nullable=True),
        sa.Column("status", sa.TEXT(), server_default="AppliedWating", nullable=False),
        sa.Column(
            "work_now", sa.BOOLEAN(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column("wallet", sa.TEXT(), nullable=True),
        sa.Column("interval_id", sa.BIGINT(), nullable=True),
        sa.Column("role_id", sa.BIGINT(), nullable=True),
        sa.Column("manager_id", sa.BIGINT(), nullable=True),
        sa.ForeignKeyConstraint(["interval_id"], ["intervals.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["manager_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("users")
