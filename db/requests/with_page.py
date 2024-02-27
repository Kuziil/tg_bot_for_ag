import datetime as dt

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PagesORM, PagesIntervalsORM, UsersORM, TgsORM, ShiftsORM


async def get_pages_with_inter_users_tgs_by_user_tg_id(
    session: AsyncSession,
    user_tg_id: int,
):
    date = dt.date.today()
    result: Result = await session.execute(
        select(PagesORM)
        .join(PagesIntervalsORM, PagesORM.id == PagesIntervalsORM.page_id)
        .join(UsersORM, PagesIntervalsORM.user_id == UsersORM.id)
        .options(
            joinedload(PagesORM.model),
            selectinload(PagesORM.intervals_details).options(
                joinedload(PagesIntervalsORM.interval),
                joinedload(PagesIntervalsORM.user).selectinload(UsersORM.tgs),
                selectinload(PagesIntervalsORM.shifts),
            ),
        )
        .filter(
            UsersORM.tgs.any(user_tg_id=user_tg_id),
        )
    )
    pages: list[PagesORM] = result.scalars().all()
    return pages


async def test_123(
    session: AsyncSession,
):
    result: Result = await session.execute(
        select(PagesIntervalsORM)
        .join(ShiftsORM, ShiftsORM.page_interval_id == PagesIntervalsORM.id)
        .options(
            selectinload(PagesIntervalsORM.shifts),
        )
    )
    pages_intervals: list[PagesIntervalsORM] = result.scalars().all()
    return pages_intervals
