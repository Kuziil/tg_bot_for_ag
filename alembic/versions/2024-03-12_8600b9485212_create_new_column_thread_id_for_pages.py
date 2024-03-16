"""create new column thread_id for pages

Revision ID: 8600b9485212
Revises: 11a53a0434d4
Create Date: 2024-03-12 12:51:30.970392

"""

import sqlalchemy as sa
from alembic import op

revision = "8600b9485212"
down_revision = "11a53a0434d4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages", sa.Column("thread_id", sa.BIGINT(), nullable=True))


def downgrade():
    op.drop_column("pages", "thread_id")
