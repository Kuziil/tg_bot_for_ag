"""Create models

Revision ID: c2015e75525b
Revises: fc248bc57da4
Create Date: 2024-02-16 07:21:04.753665

"""

from alembic import op
import sqlalchemy as sa


revision = "c2015e75525b"
down_revision = "fc248bc57da4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "models",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("models")
