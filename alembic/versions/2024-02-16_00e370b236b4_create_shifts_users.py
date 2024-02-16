"""create shifts users

Revision ID: 00e370b236b4
Revises: 9c8334d7a0b4
Create Date: 2024-02-16 20:33:30.411363

"""

from alembic import op
import sqlalchemy as sa


revision = "00e370b236b4"
down_revision = "9c8334d7a0b4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "shifts_users",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("shift_id", sa.BIGINT(), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["shift_id"], ["shifts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("shift_id", "user_id", name="idx_unique_shift_user"),
    )


def downgrade():
    op.drop_table("shifts_users")
