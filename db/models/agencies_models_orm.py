from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk

if TYPE_CHECKING:
    from .agencies_orm import AgenciesORM
    from .models_orm import ModelsORM


class AgenciesModelsORM(Base):
    __tablename__ = "agencies_models"
    __table_args__ = (
        UniqueConstraint(
            "agency_id",
            "model_id",
            name="idx_unique_agency_model",
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
    model_id: Mapped[int] = mapped_column(
        ForeignKey(
            "models.id",
            ondelete="CASCADE",
        ),
    )

    # relationships
    agency: Mapped["AgenciesORM"] = relationship(
        back_populates="models_details",
    )
    model: Mapped["ModelsORM"] = relationship(
        back_populates="agencies_details",
    )
