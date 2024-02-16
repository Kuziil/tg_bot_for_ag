from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import false, text

from db.models.base import Base
from db.models.types import intpk, strtext, boolbool, intbigint, floatnum

if TYPE_CHECKING:
    from db.models.models_orm import ModelsORM
    from db.models.users_orm import UsersORM


class PagesORM(Base):
    __tablename__ = "pages"

    id: Mapped[intpk]
    vip: Mapped[boolbool]
    sales_commision: Mapped[floatnum]
    work_same_time: Mapped[intbigint] = mapped_column(
        server_default=text(f"{1}"),
        default=text(f"{1}"),
    )
    page_link: Mapped[strtext | None]
    senior_id: Mapped[intbigint | None] = mapped_column(
        ForeignKey(
            column="users.id",
            ondelete="CASCADE",
        ),
    )
    model_id: Mapped[intbigint] = mapped_column(
        ForeignKey(
            column="models.id",
            ondelete="CASCADE",
        ),
    )
    seniors: Mapped["UsersORM"] = relationship(
        back_populates="pages",
    )
    model: Mapped["ModelsORM"] = relationship(
        back_populates="pages",
    )
