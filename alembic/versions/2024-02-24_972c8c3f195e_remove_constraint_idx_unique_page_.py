"""remove constraint idx_unique_page_interval add idx_unique_page_interval_user_lineup

Revision ID: 972c8c3f195e
Revises: 9b706889e5a5
Create Date: 2024-02-24 15:47:52.930192

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "972c8c3f195e"
down_revision = "9b706889e5a5"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("idx_unique_page_interval", "pages_intervals", type_="unique")
    op.create_unique_constraint(
        "idx_unique_page_interval_user_lineup",
        "pages_intervals",
        ["page_id", "interval_id", "user_id", "lineup"],
    )


def downgrade():
    op.drop_constraint(
        "idx_unique_page_interval_user_lineup", "pages_intervals", type_="unique"
    )
    op.create_unique_constraint(
        "idx_unique_page_interval", "pages_intervals", ["page_id", "interval_id"]
    )
