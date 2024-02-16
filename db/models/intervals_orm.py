from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped

from db.models.base import Base
from db.models.types import intpk, ttext, ddate

if TYPE_CHECKING:
    pass


class IntervalsORM(Base):
    __tablename__ = "intervals"

    id: Mapped[intpk]
    title: Mapped[ttext]
    start_at: Mapped[ddate]
    end_at: Mapped[ddate]
