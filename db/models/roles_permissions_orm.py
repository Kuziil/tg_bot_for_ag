from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, intbigint

if TYPE_CHECKING:
    from db.models.roles_orm import RolesORM
    from db.models.permissions_orm import PermissionsORM


class RolesPermissionsORM(Base):
    __tablename__ = "roles_permissions"
    __table_args__ = (
        UniqueConstraint(
            "role_id",
            "permissions_id",
            name="idx_unique_role_permission",
        ),
    )

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
    # association between Assocation -> Roles
    role: Mapped["RolesORM"] = relationship(
        back_populates="permissions_details",
    )
    # association between Assocation -> Permissions
    permission: Mapped["PermissionsORM"] = relationship(
        back_populates="roles_details",
    )
