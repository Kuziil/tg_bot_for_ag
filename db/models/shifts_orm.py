from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, dtdate, intbigint
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .pages_intervals_orm import PagesIntervalsORM
    from .users_orm import UsersORM
    from .earnings_orm import EarningsORM


class ShiftsORM(Base):
    __tablename__ = "shifts"

    # columns
    id: Mapped[intpk]
    date_shift: Mapped[dtdate]
    page_interval_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "pages_intervals.id",
            ondelete="CASCADE",
        ),
    )
    replacement_id: Mapped[intbigint | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    # relationships
    page_interval: Mapped["PagesIntervalsORM"] = relationship(
        back_populates="shifts",
    )
    # users: Mapped[list["UsersORM"]] = relationship(
    #     secondary="shifts_users",
    #     back_populates="shifts",
    # )
    replacement: Mapped["UsersORM"] = relationship(
        back_populates="shifts",
    )
    earnings: Mapped[list["EarningsORM"]] = relationship(
        back_populates="shift",
    )
