"""remove title from intervals

Revision ID: 29e018e076a6
Revises: 352d7f8e92c9
Create Date: 2024-02-20 07:54:53.257613

"""

from alembic import op
import sqlalchemy as sa


revision = "29e018e076a6"
down_revision = "352d7f8e92c9"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("intervals", "title")


def downgrade():
    op.add_column(
        "intervals", sa.Column("title", sa.TEXT(), autoincrement=False, nullable=False)
    )
