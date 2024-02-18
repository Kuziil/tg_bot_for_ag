"""replase type for amount to bigint

Revision ID: 127568d2aa3c
Revises: 49fbd099e310
Create Date: 2024-02-18 19:38:19.025246

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "127568d2aa3c"
down_revision = "49fbd099e310"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "fines",
        "amount",
        existing_type=sa.NUMERIC(),
        type_=sa.BIGINT(),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "fines",
        "amount",
        existing_type=sa.BIGINT(),
        type_=sa.NUMERIC(),
        existing_nullable=False,
    )
