from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, strtext, dtdate

if TYPE_CHECKING:
    from .users_orm import UsersORM

    pass


class IntervalsORM(Base):
    __tablename__ = "intervals"

    id: Mapped[intpk]
    title: Mapped[strtext]
    start_at: Mapped[dtdate]
    end_at: Mapped[dtdate]

    users: Mapped["UsersORM"] = relationship(
        back_populates="interval",
    )
