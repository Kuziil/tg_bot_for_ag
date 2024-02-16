from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, ttext

if TYPE_CHECKING:
    from db.models.models_orm import ModelsORM
    from db.models.agencies_models_orm import AgenciesModelsORM


class ModelsORM(Base):
    __tablename__ = "models"

    id: Mapped[intpk]
    title: Mapped[ttext]
    description: Mapped[ttext | None]
    agencies: Mapped[list["ModelsORM"]] = relationship(
        secondary="models_agencies",
        back_populates="models",
    )
    agencies_details: Mapped[list["AgenciesModelsORM"]] = relationship(
        back_populates="model",
    )
