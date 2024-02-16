from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, intbigint

if TYPE_CHECKING:
    from .shifts_orm import ShiftsORM
    from .users_orm import UsersORM
    from .earnings_orm import EarningsORM


class ShiftsUsersORM(Base):
    __tablename__ = "shifts_users"
    __table_args__ = (
        UniqueConstraint(
            "shift_id",
            "user_id",
            name="idx_unique_shift_user",
        ),
    )

    id: Mapped[intpk]
    shift_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "shifts.id",
            ondelete="CASCADE",
        ),
    )
    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )

    shift: Mapped["ShiftsORM"] = relationship(
        back_populates="users_details",
    )
    user: Mapped["UsersORM"] = relationship(
        back_populates="shifts_details",
    )
    earning: Mapped["EarningsORM"] = relationship(
        back_populates="shifts_users",
    )
