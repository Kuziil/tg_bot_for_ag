"""remove models_users

Revision ID: e06d40d15b1e
Revises: 29e018e076a6
Create Date: 2024-02-20 11:51:26.614132

"""

from alembic import op
import sqlalchemy as sa


revision = "e06d40d15b1e"
down_revision = "29e018e076a6"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("models_users")


def downgrade():
    op.create_table(
        "models_users",
        sa.Column(
            "id",
            sa.BIGINT(),
            sa.Identity(
                always=True,
                start=1,
                increment=1,
                minvalue=1,
                maxvalue=9223372036854775807,
                cycle=False,
                cache=1,
            ),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("model_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["model_id"],
            ["models.id"],
            name="models_users_model_id_fkey",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="models_users_user_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="models_users_pkey"),
        sa.UniqueConstraint("user_id", "model_id", name="idx_unique_models_users"),
    )
