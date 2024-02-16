from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, strtext, dtdate, floatnum, intbigint
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey, UniqueConstraint

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

    user: Mapped["UsersORM"] = relationship(
        back_populates="agencies_details",
    )
    agency: Mapped["AgenciesORM"] = relationship(
        back_populates="users_details",
    )
