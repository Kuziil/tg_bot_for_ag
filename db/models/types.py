from typing import Annotated
from datetime import datetime

from sqlalchemy import Identity, text, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import TEXT, BIGINT, DATE, BOOLEAN

created_at = Annotated[
    datetime,
    mapped_column(
        DATE,
        server_default=func.now(),
        default=datetime.utcnow,
    ),
]
dtdate = Annotated[datetime, mapped_column(DATE)]
intpk = Annotated[int, mapped_column(BIGINT, Identity(always=True), primary_key=True)]
intbigint = Annotated[int, mapped_column(BIGINT)]
strtext = Annotated[str, mapped_column(TEXT)]
boolbool = Annotated[bool, mapped_column(BOOLEAN)]
