"""create agencies users

Revision ID: 991e543e53a8
Revises: f74f4a0e8dc2
Create Date: 2024-02-16 22:30:41.752480

"""

from alembic import op
import sqlalchemy as sa


revision = "991e543e53a8"
down_revision = "f74f4a0e8dc2"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agencies_users",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("agency_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["agency_id"], ["agencies.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "agency_id", name="idx_unique_agency_users"),
    )


def downgrade():
    op.drop_table("agencies_users")
