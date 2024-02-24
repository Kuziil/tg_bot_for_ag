from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, strtext, intbigint

if TYPE_CHECKING:
    from .agencies_pages_orm import AgenciesPagesORM
    from .agencies_users_orm import AgenciesUsersORM


class AgenciesORM(Base):
    __tablename__ = "agencies"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext]
    main_tg_bot: Mapped[intbigint] = mapped_column(unique=True)
    test_tg_bot: Mapped[intbigint]

    # relationships
    # models: Mapped[list["ModelsORM"]] = relationship(
    #     secondary="agencies_models",
    #     back_populates="agencies",
    # )
    pages_details: Mapped[list["AgenciesPagesORM"]] = relationship(
        back_populates="agency",
    )
    users_details: Mapped[list["AgenciesUsersORM"]] = relationship(
        back_populates="agency",
    )
    # users: Mapped[list["UsersORM"]] = relationship(
    #     secondary="agencies_users",
    #     back_populates="agencies",
    # )
