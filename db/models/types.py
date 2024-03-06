from typing import Annotated
from datetime import datetime, date

from sqlalchemy import Identity, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import (
    TEXT,
    BIGINT,
    BOOLEAN,
    TIMESTAMP,
    DATE,
)

created_at = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        default=datetime.utcnow,
    ),
]
dtdate = Annotated[
    date,
    mapped_column(
        DATE,
    ),
]
dtdatetime = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
    ),
]
intpk = Annotated[
    int,
    mapped_column(
        BIGINT,
        Identity(always=True),
        primary_key=True,
    ),
]
intbigint = Annotated[
    int,
    mapped_column(
        BIGINT,
    ),
]
strtext = Annotated[
    str,
    mapped_column(
        TEXT,
    ),
]
boolbool = Annotated[
    bool,
    mapped_column(
        BOOLEAN,
    ),
]
