from uuid import uuid4

from sqlalchemy.dialects.postgresql import TEXT, UUID, INTEGER
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


from db.base import Base


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Agencies(Base):
    __tablename__ = "agencies"

    agency_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    titel: Mapped[str] = mapped_column(
        TEXT,
        nullable=False
    )
    tg_bot_id: Mapped[int] = mapped_column(
        INTEGER
    )
    test_tg_bot: Mapped[int] = mapped_column(
        INTEGER
    )
