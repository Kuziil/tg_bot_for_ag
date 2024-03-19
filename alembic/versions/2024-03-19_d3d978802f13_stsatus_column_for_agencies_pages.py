"""Status column for agencies_pages

Revision ID: d3d978802f13
Revises: 99255d91a90c
Create Date: 2024-03-19 09:48:51.764849

"""

from alembic import op
import sqlalchemy as sa


revision = "d3d978802f13"
down_revision = "99255d91a90c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("agencies_pages", sa.Column("status", sa.TEXT(), nullable=True))


def downgrade():
    op.drop_column("agencies_pages", "status")
