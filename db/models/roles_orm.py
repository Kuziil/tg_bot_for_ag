from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, strtext

if TYPE_CHECKING:
    from db.models.permissions_orm import PermissionsORM
    from db.models.roles_permissions_orm import RolesPermissionsORM
    from db.models.users_orm import UsersORM


class RolesORM(Base):
    __tablename__ = "roles"

    id: Mapped[intpk]
    title: Mapped[strtext] = mapped_column(unique=True)
    permissions: Mapped[list["PermissionsORM"]] = relationship(
        secondary="roles_permissions",
        back_populates="roles",
    )
    permissions_details: Mapped[list["RolesPermissionsORM"]] = relationship(
        back_populates="role",
    )
    users: Mapped["UsersORM"] = relationship(
        back_populates="role",
    )
