"""create intervals

Revision ID: 5456b4bc00ae
Revises: 44cd25f1d9a6
Create Date: 2024-02-16 09:44:56.050642

"""

import sqlalchemy as sa
from alembic import op

revision = "5456b4bc00ae"
down_revision = "44cd25f1d9a6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "intervals",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.Column("start_at", sa.DATE(), nullable=False),
        sa.Column("end_at", sa.DATE(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("intervals")
