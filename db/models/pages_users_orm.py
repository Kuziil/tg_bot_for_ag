from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import Base
from db.models.types import intpk, intbigint

if TYPE_CHECKING:
    from .users_orm import UsersORM
    from .pages_orm import PagesORM

    pass


class PagesUsersORM(Base):
    __tablename__ = "pages_users"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "page_id",
            name="idx_unique_page_users",
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
    page_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            "pages.id",
            ondelete="CASCADE",
        ),
    )

    # relationships
    user: Mapped["UsersORM"] = relationship(
        back_populates="pages_details",
    )
    page: Mapped["PagesORM"] = relationship(
        back_populates="users_details",
    )
