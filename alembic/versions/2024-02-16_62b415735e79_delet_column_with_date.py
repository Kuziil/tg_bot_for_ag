"""delet column with date

Revision ID: 62b415735e79
Revises: b9980c7dd8d5
Create Date: 2024-02-16 17:26:10.280560

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62b415735e79"
down_revision = "b9980c7dd8d5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("intervals", "start_at")
    op.drop_column("intervals", "end_at")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "intervals", sa.Column("end_at", sa.DATE(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "intervals",
        sa.Column("start_at", sa.DATE(), autoincrement=False, nullable=False),
    )
    # ### end Alembic commands ###
