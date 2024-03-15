from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, strtext

if TYPE_CHECKING:
    from db.models.permissions_orm import PermissionsORM
    from db.models.users_orm import UsersORM


class RolesORM(Base):
    __tablename__ = "roles"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext] = mapped_column(unique=True)

    # relationships
    permissions: Mapped[list["PermissionsORM"]] = relationship(
        secondary="roles_permissions",
        back_populates="roles",
    )
    users: Mapped["UsersORM"] = relationship(
        back_populates="role",
    )
