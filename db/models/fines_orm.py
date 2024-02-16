from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, strtext, dtdate, floatnum, intbigint
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .users_orm import UsersORM

    pass


class FinesORM(Base):
    __tablename__ = "fines"

    # columns
    id: Mapped[intpk]
    date_fine: Mapped[dtdate] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    description: Mapped[strtext | None]
    amount: Mapped[floatnum]
    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )

    # relationships
    user: Mapped["UsersORM"] = relationship(
        back_populates="fines",
    )
