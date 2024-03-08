"""create roles permissions

Revision ID: 44cd25f1d9a6
Revises: 17434961e176
Create Date: 2024-02-16 09:23:08.372142

"""

import sqlalchemy as sa
from alembic import op

revision = "44cd25f1d9a6"
down_revision = "17434961e176"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "roles_permissions",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("role_id", sa.BIGINT(), nullable=False),
        sa.Column("permissions_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(
            ["permissions_id"], ["permissions.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "role_id", "permissions_id", name="idx_unique_role_permission"
        ),
    )


def downgrade():
    op.drop_table("roles_permissions")
