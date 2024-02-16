from typing import Annotated
from datetime import datetime

from sqlalchemy import Identity, text
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import TEXT, BIGINT, DATE

created_at = Annotated[datetime, mapped_column(
    DATE, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))]
intpk = Annotated[int, mapped_column(
    BIGINT, Identity(always=True), primary_key=True)]
bigint = Annotated[int, mapped_column(BIGINT)]
ttext = Annotated[str, mapped_column(TEXT)]
