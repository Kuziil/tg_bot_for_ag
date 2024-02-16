from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false

from db.models.base import Base
from db.models.types import intpk, strtext, boolbool, intbigint

if TYPE_CHECKING:
    from db.models.intervals_orm import IntervalsORM
    from db.models.roles_orm import RolesORM
    from db.models.users_orm import UsersORM


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[strtext | None]
    emoji: Mapped[strtext | None]
    status: Mapped[strtext] = mapped_column(
        server_default="AppliedWating",
        default="AppliedWating",
    )
    work_now: Mapped[boolbool] = mapped_column(
        server_default=false(),
        default=False,
    )
    wallet: Mapped[strtext | None]
    interval_id: Mapped[intbigint | None] = mapped_column(
        ForeignKey(
            "intervals.id",
            ondelete="CASCADE",
        )
    )
    role_id: Mapped[intbigint | None] = mapped_column(
        ForeignKey(
            "roles.id",
            ondelete="CASCADE",
        ),
    )
    manager_id: Mapped[intbigint | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    interval: Mapped["IntervalsORM"] = relationship(
        back_populates="users",
    )
    role: Mapped["RolesORM"] = relationship(
        back_populates="users",
    )
    manager: Mapped["UsersORM"] = relationship(
        back_populates="users",
    )
