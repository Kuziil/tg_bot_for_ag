"""replase type for dirty to bigint

Revision ID: 352d7f8e92c9
Revises: 127568d2aa3c
Create Date: 2024-02-18 19:41:30.014177

"""

from alembic import op
import sqlalchemy as sa


revision = "352d7f8e92c9"
down_revision = "127568d2aa3c"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "earnings",
        "dirty",
        existing_type=sa.NUMERIC(),
        type_=sa.BIGINT(),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "earnings",
        "dirty",
        existing_type=sa.BIGINT(),
        type_=sa.NUMERIC(),
        existing_nullable=False,
    )
