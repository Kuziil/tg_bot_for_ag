"""remove shifts_users

Revision ID: 0d15f56ad462
Revises: d156ac3e9a6c
Create Date: 2024-02-26 10:18:20.290432

"""

import sqlalchemy as sa
from alembic import op

revision = "0d15f56ad462"
down_revision = "d156ac3e9a6c"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("earnings_shift_user_id_fkey", "earnings", type_="foreignkey")
    op.drop_table("shifts_users")
    op.add_column("earnings", sa.Column("shift_id", sa.BIGINT(), nullable=False))
    op.create_foreign_key(
        None, "earnings", "shifts", ["shift_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("earnings", "shift_user_id")


def downgrade():
    op.add_column(
        "earnings",
        sa.Column("shift_user_id", sa.BIGINT(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "earnings", type_="foreignkey")
    op.create_foreign_key(
        "earnings_shift_user_id_fkey",
        "earnings",
        "shifts_users",
        ["shift_user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("earnings", "shift_id")
    op.create_table(
        "shifts_users",
        sa.Column(
            "id",
            sa.BIGINT(),
            sa.Identity(
                always=True,
                start=1,
                increment=1,
                minvalue=1,
                maxvalue=9223372036854775807,
                cycle=False,
                cache=1,
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("shift_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["shift_id"],
            ["shifts.id"],
            name="shifts_users_shift_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="shifts_users_user_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="shifts_users_pkey"),
        sa.UniqueConstraint("shift_id", "user_id", name="idx_unique_shift_user"),
    )
