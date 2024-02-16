"""create earnings

Revision ID: cbf3e2706407
Revises: 00e370b236b4
Create Date: 2024-02-16 22:02:33.936773

"""

from alembic import op
import sqlalchemy as sa


revision = "cbf3e2706407"
down_revision = "00e370b236b4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "earnings",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column(
            "confirm", sa.BOOLEAN(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column("dirty", sa.NUMERIC(), nullable=False),
        sa.Column("shift_user_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["shift_user_id"], ["shifts_users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("earnings")
