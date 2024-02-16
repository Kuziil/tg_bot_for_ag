from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, strtext

if TYPE_CHECKING:
    from db.models.agencies_orm import AgenciesORM
    from db.models.agencies_models_orm import AgenciesModelsORM
    from db.models.pages_orm import PagesORM


class ModelsORM(Base):
    __tablename__ = "models"

    id: Mapped[intpk]
    title: Mapped[strtext]
    description: Mapped[strtext | None]
    agencies: Mapped[list["AgenciesORM"]] = relationship(
        secondary="agencies_models",
        back_populates="models",
    )
    agencies_details: Mapped[list["AgenciesModelsORM"]] = relationship(
        back_populates="model",
    )
    pages: Mapped["PagesORM"] = relationship(
        back_populates="model",
    )
