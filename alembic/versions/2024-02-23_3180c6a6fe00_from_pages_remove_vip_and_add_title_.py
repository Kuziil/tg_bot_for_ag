"""from pages remove vip and add title, type_in_agency, subscription_type, subscription_type

Revision ID: 3180c6a6fe00
Revises: 81aa10435585
Create Date: 2024-02-23 23:04:38.869240

"""

from alembic import op
import sqlalchemy as sa


revision = "3180c6a6fe00"
down_revision = "81aa10435585"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages", sa.Column("title", sa.TEXT(), nullable=False))
    op.add_column("pages", sa.Column("type_in_agency", sa.TEXT(), nullable=False))
    op.add_column("pages", sa.Column("subscription_type", sa.TEXT(), nullable=False))
    op.add_column("pages", sa.Column("platform", sa.TEXT(), nullable=False))
    op.drop_column("pages", "vip")


def downgrade():
    op.add_column(
        "pages", sa.Column("vip", sa.BOOLEAN(), autoincrement=False, nullable=False)
    )
    op.drop_column("pages", "platform")
    op.drop_column("pages", "subscription_type")
    op.drop_column("pages", "type_in_agency")
    op.drop_column("pages", "title")
