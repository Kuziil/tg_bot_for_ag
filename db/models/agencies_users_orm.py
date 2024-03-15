from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, intbigint, strtext

if TYPE_CHECKING:
    from .users_orm import UsersORM
    from .agencies_orm import AgenciesORM

    pass


class AgenciesUsersORM(Base):
    __tablename__ = "agencies_users"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "agency_id",
            name="idx_unique_agency_users",
        ),
    )

    # columns
    id: Mapped[intpk]
    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    agency_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "agencies.id",
            ondelete="CASCADE",
        ),
    )
    status: Mapped[strtext | None]

    # relationships
    user: Mapped["UsersORM"] = relationship(
        back_populates="agencies_details",
    )
    agency: Mapped["AgenciesORM"] = relationship(
        back_populates="users_details",
    )
