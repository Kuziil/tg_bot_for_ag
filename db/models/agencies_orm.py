from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, strtext, intbigint

if TYPE_CHECKING:
    from .models_orm import ModelsORM
    from .agencies_models_orm import AgenciesModelsORM
    from .agencies_users_orm import AgenciesUsersORM
    from .users_orm import UsersORM


class AgenciesORM(Base):
    __tablename__ = "agencies"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext]
    tg_bot: Mapped[intbigint]
    test_tg_bot: Mapped[intbigint]

    # relationships
    models: Mapped[list["ModelsORM"]] = relationship(
        secondary="agencies_models",
        back_populates="agencies",
    )
    models_details: Mapped[list["AgenciesModelsORM"]] = relationship(
        back_populates="agency",
    )
    users_details: Mapped[list["AgenciesUsersORM"]] = relationship(
        back_populates="agency",
    )
    users: Mapped[list["UsersORM"]] = relationship(
        secondary="agencies_users",
        back_populates="agencies",
    )
