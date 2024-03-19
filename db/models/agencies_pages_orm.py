from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, strtext

if TYPE_CHECKING:
    from .agencies_orm import AgenciesORM
    from .models_orm import PagesORM


class AgenciesPagesORM(Base):
    __tablename__ = "agencies_pages"
    __table_args__ = (
        UniqueConstraint(
            "agency_id",
            "page_id",
            name="idx_unique_agency_page",
        ),
    )

    # columns
    id: Mapped[intpk]
    agency_id: Mapped[int] = mapped_column(
        ForeignKey(
            "agencies.id",
            ondelete="CASCADE",
        ),
    )
    page_id: Mapped[int] = mapped_column(
        ForeignKey(
            "pages.id",
            ondelete="CASCADE",
        ),
    )
    status: Mapped[strtext | None]

    # relationships
    agency: Mapped["AgenciesORM"] = relationship(
        back_populates="pages_details",
    )
    page: Mapped["PagesORM"] = relationship(
        back_populates="agencies_details",
    )
