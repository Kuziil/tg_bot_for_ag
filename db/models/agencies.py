from sqlalchemy.orm import Mapped

from db.models.base import Base
from db.models.types import intpk, ttext, bigint


class Agencies(Base):
    __tablename__ = "agencies"

    id: Mapped[intpk]
    title: Mapped[ttext]
    tg_bot_id: Mapped[bigint]
    test_tg_bot: Mapped[bigint]
