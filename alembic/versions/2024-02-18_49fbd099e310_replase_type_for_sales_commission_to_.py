"""replase type for sales_commission to bigint and rename

Revision ID: 49fbd099e310
Revises: 27b91351ecd9
Create Date: 2024-02-18 19:32:41.777004

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "49fbd099e310"
down_revision = "27b91351ecd9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages", sa.Column("sales_commission", sa.BIGINT(), nullable=False))
    op.drop_column("pages", "sales_commision")
    # ### end Alembic commands ###


def downgrade():
    op.add_column(
        "pages",
        sa.Column("sales_commision", sa.NUMERIC(), autoincrement=False, nullable=False),
    )
    op.drop_column("pages", "sales_commission")
