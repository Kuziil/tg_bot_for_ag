from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from db.models.types import intpk, ttext

if TYPE_CHECKING:
    pass


class RolesORM(Base):
    __tablename__ = "roles"

    id: Mapped[intpk]
    title: Mapped[ttext] = mapped_column(unique=True)
