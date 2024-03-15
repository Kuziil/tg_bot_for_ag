from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from db.models.types import intpk, intbigint

if TYPE_CHECKING:
    pass


class RolesPermissionsORM(Base):
    __tablename__ = "roles_permissions"
    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permissions_id",
            name="idx_unique_role_permission",
        ),
    )

    # columns
    id: Mapped[intpk]
    role_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            column="roles.id",
            ondelete="CASCADE",
        ),
    )
    permissions_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            column="permissions.id",
            ondelete="CASCADE",
        ),
    )
