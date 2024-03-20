from typing import Sequence

from sqlalchemy import select, extract
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    selectinload,
    joinedload,
)

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
    pages: Sequence[PagesORM] = result.scalars().all()
    return pages


async def get_all_pages(
        session: AsyncSession,
        user_tg_id: int,
        agency_id: int
):
    stmt = select(PagesORM).options(
        selectinload(PagesORM.agencies_details),
        selectinload(PagesORM.intervals_details).joinedload(PagesIntervalsORM.user).selectinload(UsersORM.tgs)
    ).filter(
        PagesORM.agencies_details.any(agency_id=agency_id, status="work_now"),
        UsersORM.role_id == 3,
        UsersORM.tgs.any(user_tg_id=user_tg_id)
    )
    result: Result = await session.execute(stmt)
    pages: Sequence[PagesORM] = result.scalars().all()
    return pages
