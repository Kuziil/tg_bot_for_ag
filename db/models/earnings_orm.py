from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import false

from db.models.base import Base
from db.models.types import intpk, dtdate, intbigint, boolbool, floatnum
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .shifts_users_orm import ShiftsUsersORM

    pass


class EarningsORM(Base):
    __tablename__ = "earnings"

    # columns
    id: Mapped[intpk]
    confirm: Mapped[boolbool] = mapped_column(
        server_default=false(),
        default=False,
    )
    dirty: Mapped[floatnum]
    shift_user_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "shifts_users.id",
            ondelete="CASCADE",
        )
    )

    # relationships
    shifts_users: Mapped[list["ShiftsUsersORM"]] = relationship(
        back_populates="earning",
    )
