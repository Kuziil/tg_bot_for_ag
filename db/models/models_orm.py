from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, strtext

if TYPE_CHECKING:
    from db.models.pages_orm import PagesORM


class ModelsORM(Base):
    __tablename__ = "models"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext]
    description: Mapped[strtext | None]

    # relationships
    pages: Mapped["PagesORM"] = relationship(
        back_populates="model",
    )
