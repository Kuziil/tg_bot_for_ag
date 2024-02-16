from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, strtext, intbigint

if TYPE_CHECKING:
    from db.models.models_orm import ModelsORM
    from db.models.agencies_models_orm import AgenciesModelsORM


class AgenciesORM(Base):
    __tablename__ = "agencies"

    id: Mapped[intpk]
    title: Mapped[strtext]
    tg_bot_id: Mapped[intbigint]
    test_tg_bot: Mapped[intbigint]
    models: Mapped[list["ModelsORM"]] = relationship(
        secondary="models_agencies",
        back_populates="agencies",
    )
    models_details: Mapped[list["AgenciesModelsORM"]] = relationship(
        back_populates="agency",
    )
