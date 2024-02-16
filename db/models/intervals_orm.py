from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, strtext, dttime

if TYPE_CHECKING:
    from .users_orm import UsersORM
    from .pages_intervals_orm import PagesIntervalsORM
    from .pages_orm import PagesORM


class IntervalsORM(Base):
    __tablename__ = "intervals"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext]
    start_at: Mapped[dttime]
    end_at: Mapped[dttime]

    # relationships
    users: Mapped["UsersORM"] = relationship(
        back_populates="interval",
    )
    pages: Mapped[list["PagesORM"]] = relationship(
        secondary="pages_intervals",
        back_populates="intervals",
    )
    pages_details: Mapped[list["PagesIntervalsORM"]] = relationship(
        back_populates="interval",
    )
