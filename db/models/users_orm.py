from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false

from db.models.base import Base
from db.models.types import intpk, strtext, boolbool, intbigint

if TYPE_CHECKING:
    from db.models.intervals_orm import IntervalsORM
    from db.models.roles_orm import RolesORM
    from db.models.tgs_orm import TgsORM
    from db.models.pages_orm import PagesORM


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
    # relationship between Users -> Intervals
    interval: Mapped["IntervalsORM"] = relationship(
        back_populates="users",
    )
    # relationship between Users -> Roles
    role: Mapped["RolesORM"] = relationship(
        back_populates="users",
    )
    # relationship between Users.manager_id -> Users.id
    user: Mapped["UsersORM"] = relationship(
        back_populates="manager",
    )
    # relationship between Users.id -> Users.manager_id
    manager: Mapped["UsersORM"] = relationship(
        back_populates="user",
        remote_side="UsersORM.id",
    )
    # relationship between Users -> Tgs
    tgs: Mapped[list["TgsORM"]] = relationship(
        back_populates="user",
    )
    # relationship between Users -> Pages
    pages: Mapped["PagesORM"] = relationship(
        back_populates="seniors",
    )
