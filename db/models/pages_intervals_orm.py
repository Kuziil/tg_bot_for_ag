from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, intbigint
from sqlalchemy import ForeignKey, UniqueConstraint

if TYPE_CHECKING:
    from .intervals_orm import IntervalsORM
    from .pages_orm import PagesORM

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

    page: Mapped["PagesORM"] = relationship(
        back_populates="intervals_details",
    )
    interval: Mapped["IntervalsORM"] = relationship(
        back_populates="pages_details",
    )
