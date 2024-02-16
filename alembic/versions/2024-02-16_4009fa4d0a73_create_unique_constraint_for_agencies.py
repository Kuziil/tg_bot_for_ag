"""create unique constraint for agencies

Revision ID: 4009fa4d0a73
Revises: 04efc47a5177
Create Date: 2024-02-16 22:51:46.967838

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4009fa4d0a73"
down_revision = "04efc47a5177"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        "idx_unique_id_tg_bot_id", "agencies", ["id", "tg_bot_id"]
    )


def downgrade():
    op.drop_constraint("idx_unique_id_tg_bot_id", "agencies", type_="unique")
