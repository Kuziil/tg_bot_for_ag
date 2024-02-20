"""remove pages_users

Revision ID: 06772c1cb8f5
Revises: e01c93ac2392
Create Date: 2024-02-20 18:51:33.834026

"""

from alembic import op
import sqlalchemy as sa


revision = "06772c1cb8f5"
down_revision = "e01c93ac2392"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("pages_users")


def downgrade():
    op.create_table(
        "pages_users",
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
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("page_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["page_id"],
            ["pages.id"],
            name="pages_users_page_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="pages_users_user_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pages_users_pkey"),
        sa.UniqueConstraint("user_id", "page_id", name="idx_unique_page_users"),
    )
