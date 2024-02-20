from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pydantic import SecretStr


class DatabaseHelper:
    def __init__(
        self,
        db_url: SecretStr,
        echo: bool = False,
        pool_size: int | None = None,
        max_overflow: int | None = None,
    ) -> None:
        self.engine = create_async_engine(
            url=str(db_url),
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )
