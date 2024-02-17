"""added uniqueness to the mian_tg_bot column

Revision ID: 4ef0f4e2e8ea
Revises: 48abe164d07e
Create Date: 2024-02-17 19:48:30.737217

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4ef0f4e2e8ea"
down_revision = "48abe164d07e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, "agencies", ["main_tg_bot"])


def downgrade():
    op.drop_constraint(None, "agencies", type_="unique")
