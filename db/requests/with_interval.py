from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import IntervalsORM


async def get_interval_by_id(
    session: AsyncSession,
    interval_id: int,
) -> IntervalsORM:
    result: Result = await session.execute(
        select(IntervalsORM).where(IntervalsORM.id == interval_id)
    )
    interval: IntervalsORM = result.scalar_one_or_none()
    return interval
