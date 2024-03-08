"""lineup for pages_intervals

Revision ID: 81aa10435585
Revises: d2cb9f9799ce
Create Date: 2024-02-23 22:14:45.794044

"""

import sqlalchemy as sa
from alembic import op

revision = "81aa10435585"
down_revision = "d2cb9f9799ce"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "pages_intervals",
        sa.Column("lineup", sa.BIGINT(), server_default="1", nullable=False),
    )


def downgrade():
    op.drop_column("pages_intervals", "lineup")
