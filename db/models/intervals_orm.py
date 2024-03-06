from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from db.models.base import Base
from db.models.types import intpk, dtdatetime

if TYPE_CHECKING:
    from .pages_intervals_orm import PagesIntervalsORM


class IntervalsORM(Base):
    __tablename__ = "intervals"

    # columns
    id: Mapped[intpk]
    start_at: Mapped[dtdatetime]
    end_at: Mapped[dtdatetime]

    # relationships
    pages_details: Mapped[list["PagesIntervalsORM"]] = relationship(
        back_populates="interval",
    )
