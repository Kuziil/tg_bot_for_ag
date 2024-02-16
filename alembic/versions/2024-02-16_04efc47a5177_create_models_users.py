"""create models users

Revision ID: 04efc47a5177
Revises: 991e543e53a8
Create Date: 2024-02-16 22:39:28.749788

"""

from alembic import op
import sqlalchemy as sa


revision = "04efc47a5177"
down_revision = "991e543e53a8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "models_users",
        sa.Column("id", sa.BIGINT(), sa.Identity(always=True), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("model_id", sa.BIGINT(), nullable=False),
        sa.ForeignKeyConstraint(["model_id"], ["models.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "model_id", name="idx_unique_models_users"),
    )


def downgrade():
    op.drop_table("models_users")
