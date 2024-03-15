from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, strtext

if TYPE_CHECKING:
    from db.models.roles_orm import RolesORM
    pass


class PermissionsORM(Base):
    __tablename__ = "permissions"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext] = mapped_column(unique=True)

    # relationships
    roles: Mapped[list["RolesORM"]] = relationship(
        secondary="roles_permissions",
        back_populates="permissions",
    )
