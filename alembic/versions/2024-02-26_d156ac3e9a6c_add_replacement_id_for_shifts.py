"""add replacement_id for shifts

Revision ID: d156ac3e9a6c
Revises: 972c8c3f195e
Create Date: 2024-02-26 10:11:46.947638

"""

import sqlalchemy as sa
from alembic import op

revision = "d156ac3e9a6c"
down_revision = "972c8c3f195e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("shifts", sa.Column("replacement_id", sa.BIGINT(), nullable=True))
    op.create_foreign_key(
        None, "shifts", "users", ["replacement_id"], ["id"], ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint(None, "shifts", type_="foreignkey")
    op.drop_column("shifts", "replacement_id")
