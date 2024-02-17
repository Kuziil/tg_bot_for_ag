from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base
from db.models.types import intpk, intbigint

if TYPE_CHECKING:
    from .users_orm import UsersORM

    pass


class TgsORM(Base):
    __tablename__ = "tgs"

    # columns
    id: Mapped[intpk]
    user_tg_id: Mapped[intbigint]
    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey(column="users.id", ondelete="CASCADE"),
    )

    # relationships
    user: Mapped["UsersORM"] = relationship(
        back_populates="tgs",
    )
