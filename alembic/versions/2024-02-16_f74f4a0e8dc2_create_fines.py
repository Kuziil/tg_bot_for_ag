"""create fines

Revision ID: f74f4a0e8dc2
Revises: cbf3e2706407
Create Date: 2024-02-16 22:18:35.286564

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f74f4a0e8dc2"
down_revision = "cbf3e2706407"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "fines",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column(
            "date_fine", sa.DATE(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.Column("amount", sa.NUMERIC(), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("fines")
