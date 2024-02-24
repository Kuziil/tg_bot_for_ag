"""remove interval_id from users

Revision ID: 9b706889e5a5
Revises: e10646485942
Create Date: 2024-02-24 12:51:33.450482

"""

from alembic import op
import sqlalchemy as sa


revision = "9b706889e5a5"
down_revision = "e10646485942"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("users_interval_id_fkey", "users", type_="foreignkey")
    op.drop_column("users", "interval_id")


def downgrade():
    op.add_column(
        "users",
        sa.Column("interval_id", sa.BIGINT(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "users_interval_id_fkey",
        "users",
        "intervals",
        ["interval_id"],
        ["id"],
        ondelete="CASCADE",
    )
