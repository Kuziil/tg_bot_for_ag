"""constraint for pages_intervals user_id nullable=True

Revision ID: e01c93ac2392
Revises: c5db8bada433
Create Date: 2024-02-20 18:11:27.166456

"""

from alembic import op
import sqlalchemy as sa


revision = "e01c93ac2392"
down_revision = "c5db8bada433"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "pages_intervals", "user_id", existing_type=sa.BIGINT(), nullable=True
    )


def downgrade():
    op.alter_column(
        "pages_intervals", "user_id", existing_type=sa.BIGINT(), nullable=False
    )
