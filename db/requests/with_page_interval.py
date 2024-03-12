from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.models import PagesIntervalsORM, UsersORM


async def get_page_user_interval_by_page_interval_id(
        session: AsyncSession,
        user_tg_id: int,
        page_interval_id: int,
):
    result: Result = await session.execute(
        select(PagesIntervalsORM).options(
            joinedload(PagesIntervalsORM.page),
            joinedload(PagesIntervalsORM.user).selectinload(UsersORM.tgs),
            joinedload(PagesIntervalsORM.interval)
        ).filter(
            PagesIntervalsORM.id == page_interval_id,
            UsersORM.tgs.any(user_tg_id=user_tg_id),
        )
    )
    page_interval: PagesIntervalsORM = result.scalar()
    return page_interval
