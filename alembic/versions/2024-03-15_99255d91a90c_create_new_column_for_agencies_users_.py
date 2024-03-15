"""create new column for agencies_users. This column is responsible for the user's status in the agency

Revision ID: 99255d91a90c
Revises: 1c4e8269e3f1
Create Date: 2024-03-15 11:13:04.577370

"""

from alembic import op
import sqlalchemy as sa


revision = "99255d91a90c"
down_revision = "1c4e8269e3f1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("agencies_users", sa.Column("status", sa.TEXT(), nullable=True))


def downgrade():
    op.drop_column("agencies_users", "status")
