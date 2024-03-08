"""new user_id column for pages_intervals

Revision ID: c5db8bada433
Revises: 3f778e74dce2
Create Date: 2024-02-20 14:53:07.200388

"""

import sqlalchemy as sa
from alembic import op

revision = "c5db8bada433"
down_revision = "3f778e74dce2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages_intervals", sa.Column("user_id", sa.BIGINT(), nullable=False))
    op.create_foreign_key(
        None, "pages_intervals", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint(None, "pages_intervals", type_="foreignkey")
    op.drop_column("pages_intervals", "user_id")
