from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, dtdate, intbigint, dtdatetime

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
    start_at: Mapped[dtdatetime | None]
    end_at: Mapped[dtdatetime | None]
    # relationships
    page_interval: Mapped["PagesIntervalsORM"] = relationship(
        back_populates="shifts",
    )
    replacement: Mapped["UsersORM"] = relationship(
        back_populates="shifts",
    )
    earnings: Mapped[list["EarningsORM"]] = relationship(
        back_populates="shift",
    )
