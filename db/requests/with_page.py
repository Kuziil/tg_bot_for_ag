import datetime as dt

from sqlalchemy import select, or_, extract
from sqlalchemy.engine import Result
from sqlalchemy.orm import (
    selectinload,
    joinedload,
    contains_eager,
    with_loader_criteria,
)
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PagesORM, PagesIntervalsORM, UsersORM, TgsORM, ShiftsORM


async def get_pages_with_inter_users_tgs_shifts_by_user_tg_id(
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
    pages: list[PagesORM] = result.scalars().all()
    return pages


async def test_123(
    session: AsyncSession,
    user_tg_id: int,
):
    month = dt.date.today().month

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


# async def test_123(
#     session: AsyncSession,
# ):
#     month = dt.date.today().month

#     result = await session.execute(
#         select(PagesIntervalsORM)
#         .options(
#             selectinload(
#                 PagesIntervalsORM.shifts.and_(
#                     extract("month", ShiftsORM.date_shift) == 1
#                 )
#             )
#         )
#         .where(PagesIntervalsORM.id < 9)
#     )
#     pages_intervals: list[PagesIntervalsORM] = result.scalars().all()
#     return pages_intervals


# async def test_123(
#     session: AsyncSession,
# ):
#     month = dt.date.today().month

#     result = await session.execute(
#         select(PagesIntervalsORM)
#         .outerjoin(PagesIntervalsORM.shifts)
#         .where(
#             (extract("month", ShiftsORM.date_shift) == 1)
#             | (ShiftsORM.date_shift == None)
#         )
#         .options(contains_eager(PagesIntervalsORM.shifts))
#         .filter(PagesIntervalsORM.user_id < 5)  # добавили фильтр по user_id
#     )
#     pages_intervals: list[PagesIntervalsORM] = result.scalars().unique().all()
#     return pages_intervals
