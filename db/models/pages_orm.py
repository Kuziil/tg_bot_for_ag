from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from db.models.base import Base
from db.models.types import (
    intpk,
    strtext,
    intbigint,
)

if TYPE_CHECKING:
    from .models_orm import ModelsORM
    from .users_orm import UsersORM
    from .pages_intervals_orm import PagesIntervalsORM
    from .agencies_pages_orm import AgenciesPagesORM


class PagesORM(Base):
    __tablename__ = "pages"

    # columns
    id: Mapped[intpk]
    title: Mapped[strtext]
    type_in_agency: Mapped[strtext]
    subscription_type: Mapped[strtext]
    platform: Mapped[strtext]
    sales_commission: Mapped[intbigint]
    work_same_time: Mapped[intbigint] = mapped_column(
        server_default=text(f"{1}"),
        default=1,
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
    thread_id: Mapped[intbigint | None]

    # relationships
    seniors: Mapped["UsersORM"] = relationship(
        back_populates="pages",
    )
    model: Mapped["ModelsORM"] = relationship(
        back_populates="pages",
    )
    intervals_details: Mapped[list["PagesIntervalsORM"]] = relationship(
        back_populates="page",
    )
    agencies_details: Mapped[list["AgenciesPagesORM"]] = relationship(
        back_populates="page",
    )
