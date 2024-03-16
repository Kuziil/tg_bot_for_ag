"""rename column thread_id to reshift_thread_id

Revision ID: 13bd61c35bfb
Revises: 8600b9485212
Create Date: 2024-03-12 23:56:07.965911

"""

import sqlalchemy as sa
from alembic import op

revision = "13bd61c35bfb"
down_revision = "8600b9485212"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages", sa.Column("reshift_thread_id", sa.BIGINT(), nullable=True))
    op.drop_column("pages", "thread_id")


def downgrade():
    op.add_column(
        "pages", sa.Column("thread_id", sa.BIGINT(), autoincrement=False, nullable=True)
    )
    op.drop_column("pages", "reshift_thread_id")
