"""Create agencies models

Revision ID: edf0d3493308
Revises: c2015e75525b
Create Date: 2024-02-16 08:22:17.060173

"""

import sqlalchemy as sa
from alembic import op

revision = "edf0d3493308"
down_revision = "c2015e75525b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agencies_models",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("agency_id", sa.BIGINT(), nullable=False),
        sa.Column("model_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["agency_id"], ["agencies.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("agency_id", "model_id", name="idx_unique_agency_model"),
    )


def downgrade():
    op.drop_table("agencies_models")
