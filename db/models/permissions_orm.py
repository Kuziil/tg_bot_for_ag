from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, ttext

if TYPE_CHECKING:
    from db.models.roles_orm import RolesORM
    from db.models.roles_permissions_orm import RolesPermissionsORM

    pass


class PermissionsORM(Base):
    __tablename__ = "permissions"

    id: Mapped[intpk]
    title: Mapped[ttext] = mapped_column(unique=True)
    roles: Mapped[list["RolesORM"]] = relationship(
        secondary="roles_permissions",
        back_populates="permissions",
    )
    roles_details: Mapped[list["RolesPermissionsORM"]] = relationship(
        back_populates="permission",
    )
