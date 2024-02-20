from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, intbigint

if TYPE_CHECKING:
    from .intervals_orm import IntervalsORM
    from .pages_orm import PagesORM
    from .shifts_orm import ShiftsORM

    pass


class PagesIntervalsORM(Base):
    __tablename__ = "pages_intervals"
    __table_args__ = (
        UniqueConstraint(
            "page_id",
            "interval_id",
            name="idx_unique_page_interval",
        ),
    )

    # columns
    id: Mapped[intpk]
    page_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            column="pages.id",
            ondelete="CASCADE",
        ),
    )
    interval_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            column="intervals.id",
            ondelete="CASCADE",
        ),
    )

    # relationships
    page: Mapped["PagesORM"] = relationship(
        back_populates="intervals_details",
    )
    interval: Mapped["IntervalsORM"] = relationship(
        back_populates="pages_details",
    )
    shifts: Mapped["ShiftsORM"] = relationship(
        back_populates="page_interval",
    )
