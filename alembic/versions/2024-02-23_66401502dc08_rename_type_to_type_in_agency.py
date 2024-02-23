"""rename type to type_in_agency

Revision ID: 66401502dc08
Revises: 7b2a44ea56cc
Create Date: 2024-02-23 22:51:28.059844

"""

from alembic import op
import sqlalchemy as sa


revision = "66401502dc08"
down_revision = "7b2a44ea56cc"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("pages", sa.Column("type_in_agency", sa.TEXT(), nullable=False))


def downgrade():
    op.drop_column("pages", "type_in_agency")
