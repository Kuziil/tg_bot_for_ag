from datetime import datetime, date
from typing import Annotated

from sqlalchemy import Identity
from sqlalchemy.dialects.postgresql import (
    TEXT,
    BIGINT,
    BOOLEAN,
    TIMESTAMP,
    DATE,
)
from sqlalchemy.orm import mapped_column

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
