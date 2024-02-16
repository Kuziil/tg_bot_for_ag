from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, dtdate, intbigint
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .pages_intervals_orm import PagesIntervalsORM

    pass


class ShiftsORM(Base):
    __tablename__ = "shifts"

    id: Mapped[intpk]
    date_shift: Mapped[dtdate]
    page_interval_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "pages_intervals.id",
            ondelete="CASCADE",
        ),
    )
    page_interval: Mapped["PagesIntervalsORM"] = relationship(
        back_populates="shifts",
    )
