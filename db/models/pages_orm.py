from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from db.models.base import Base
from db.models.types import intpk, strtext, boolbool, intbigint, floatnum

if TYPE_CHECKING:
    from .models_orm import ModelsORM
    from .users_orm import UsersORM
    from .pages_intervals_orm import PagesIntervalsORM
    from .intervals_orm import IntervalsORM


class PagesORM(Base):
    __tablename__ = "pages"

    id: Mapped[intpk]
    vip: Mapped[boolbool]
    sales_commision: Mapped[floatnum]
    work_same_time: Mapped[intbigint] = mapped_column(
        server_default=text(f"{1}"),
        default=text(f"{1}"),
    )
    page_link: Mapped[strtext | None]
    senior_id: Mapped[intbigint | None] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
        ),
    )
    model_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            column="models.id",
            ondelete="CASCADE",
        ),
    )
    seniors: Mapped["UsersORM"] = relationship(
        back_populates="pages",
    )
    model: Mapped["ModelsORM"] = relationship(
        back_populates="pages",
    )
    intervals: Mapped[list["IntervalsORM"]] = relationship(
        secondary="pages_intervals",
        back_populates="pages",
    )
    intervals_details: Mapped["PagesIntervalsORM"] = relationship(
        back_populates="page",
    )
