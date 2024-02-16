from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, strtext, dttime

if TYPE_CHECKING:
    from .users_orm import UsersORM


class IntervalsORM(Base):
    __tablename__ = "intervals"

    id: Mapped[intpk]
    title: Mapped[strtext]
    start_at: Mapped[dttime]
    end_at: Mapped[dttime]

    users: Mapped["UsersORM"] = relationship(
        back_populates="interval",
    )
