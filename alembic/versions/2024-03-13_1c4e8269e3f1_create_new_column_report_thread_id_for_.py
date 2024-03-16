"""create new column report_thread_id for pages

Revision ID: 1c4e8269e3f1
Revises: 13bd61c35bfb
Create Date: 2024-03-13 00:01:39.583596

"""

import sqlalchemy as sa
from alembic import op

revision = "1c4e8269e3f1"
down_revision = "13bd61c35bfb"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages", sa.Column("report_thread_id", sa.BIGINT(), nullable=True))


def downgrade():
    op.drop_column("pages", "report_thread_id")
