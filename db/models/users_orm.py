from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false

from db.models.base import Base
from db.models.types import intpk, strtext, boolbool, intbigint

if TYPE_CHECKING:
    from .intervals_orm import IntervalsORM
    from .roles_orm import RolesORM
    from .tgs_orm import TgsORM
    from .pages_orm import PagesORM
    from .shifts_users_orm import ShiftsUsersORM
    from .shifts_orm import ShiftsORM
    from .fines_orm import FinesORM
    from .agencies_users_orm import AgenciesUsersORM
    from .agencies_orm import AgenciesORM
    from .models_orm import ModelsORM
    from .models_users_orm import ModelsUsersORM


class UsersORM(Base):
    __tablename__ = "users"

    # columns
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

    # relationships
    interval: Mapped["IntervalsORM"] = relationship(
        back_populates="users",
    )
    role: Mapped["RolesORM"] = relationship(
        back_populates="users",
    )
    user: Mapped["UsersORM"] = relationship(
        back_populates="manager",
    )
    manager: Mapped["UsersORM"] = relationship(
        back_populates="user",
        remote_side="UsersORM.id",
    )
    tgs: Mapped[list["TgsORM"]] = relationship(
        back_populates="user",
    )
    pages: Mapped["PagesORM"] = relationship(
        back_populates="seniors",
    )
    shifts: Mapped[list["ShiftsORM"]] = relationship(
        secondary="shifts_users",
        back_populates="users",
    )
    shifts_details: Mapped[list["ShiftsUsersORM"]] = relationship(
        back_populates="user",
    )
    fines: Mapped[list["FinesORM"]] = relationship(
        back_populates="user",
    )
    agencies_details: Mapped[list["AgenciesUsersORM"]] = relationship(
        back_populates="user",
    )
    agencies: Mapped[list["AgenciesORM"]] = relationship(
        secondary="agencies_users",
        back_populates="users",
    )
    models_details: Mapped[list["ModelsUsersORM"]] = relationship(
        back_populates="user",
    )
    models: Mapped[list["ModelsORM"]] = relationship(
        secondary="models_users",
        back_populates="users",
    )
