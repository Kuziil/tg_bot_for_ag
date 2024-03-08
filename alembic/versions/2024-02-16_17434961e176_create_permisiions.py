"""create permisiions

Revision ID: 17434961e176
Revises: 487b34e5e665
Create Date: 2024-02-16 08:54:09.546186

"""

import sqlalchemy as sa
from alembic import op

revision = "17434961e176"
down_revision = "487b34e5e665"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "permissions",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )


def downgrade():
    op.drop_table("permissions")
