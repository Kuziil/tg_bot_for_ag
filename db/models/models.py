from sqlalchemy.orm import Mapped

from db.models.base import Base
from db.models.types import intpk, ttext


class ModelsORM(Base):
    __tablename__ = "models"

    id: Mapped[intpk]
    title: Mapped[ttext]
    description: Mapped[ttext | None]
