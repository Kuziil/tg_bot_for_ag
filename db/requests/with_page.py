from sqlalchemy import select, extract
from sqlalchemy.engine import Result
from sqlalchemy.orm import (
    selectinload,
    joinedload,
)
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PagesORM, PagesIntervalsORM, UsersORM, ShiftsORM


async def get_pages_by_user_tg_id(
    session: AsyncSession,
    user_tg_id: int,
    current_month: int,
):
    result: Result = await session.execute(
        select(PagesORM)
        .join(PagesIntervalsORM, PagesORM.id == PagesIntervalsORM.page_id)
        .join(UsersORM, PagesIntervalsORM.user_id == UsersORM.id)
        .options(
            joinedload(PagesORM.model),
            selectinload(PagesORM.intervals_details).options(
                joinedload(PagesIntervalsORM.interval),
                joinedload(PagesIntervalsORM.user).selectinload(UsersORM.tgs),
                selectinload(
                    PagesIntervalsORM.shifts.and_(
                        extract("month", ShiftsORM.date_shift) == current_month
                    )
                ).joinedload(ShiftsORM.replacement),
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
    user_tg_id: int,
):
    result = await session.execute(
        select(PagesORM)
        .join(PagesORM.intervals_details)
        .join(PagesIntervalsORM.user)
        .options(
            joinedload(PagesORM.model),
            selectinload(PagesORM.intervals_details).options(
                joinedload(PagesIntervalsORM.interval),
                joinedload(PagesIntervalsORM.user).selectinload(UsersORM.tgs),
                selectinload(
                    PagesIntervalsORM.shifts.and_(
                        extract("month", ShiftsORM.date_shift) == 1
                    )
                ),
            ),
        )
        .filter(
            UsersORM.tgs.any(user_tg_id=user_tg_id),
        )
    )
    pages_intervals: list[PagesIntervalsORM] = result.scalars().all()
    return pages_intervals
