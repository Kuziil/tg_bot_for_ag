from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, strtext

if TYPE_CHECKING:
    from db.models.roles_permissions_orm import RolesPermissionsORM

    pass


class PermissionsORM(Base):
    __tablename__ = "permissions"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext] = mapped_column(unique=True)

    # relationships
    roles_details: Mapped[list["RolesPermissionsORM"]] = relationship(
        back_populates="permission",
    )
