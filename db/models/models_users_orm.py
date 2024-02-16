from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, strtext, dtdate, floatnum, intbigint
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey, UniqueConstraint

if TYPE_CHECKING:
    from .users_orm import UsersORM
    from .models_orm import ModelsORM

    pass


class ModelsUsersORM(Base):
    __tablename__ = "models_users"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "model_id",
            name="idx_unique_models_users",
        ),
    )
    id: Mapped[intpk]
    user_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    model_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "models.id",
            ondelete="CASCADE",
        ),
    )
    user: Mapped["UsersORM"] = relationship(
        back_populates="models_details",
    )
    model: Mapped["ModelsORM"] = relationship(
        back_populates="users_details",
    )
