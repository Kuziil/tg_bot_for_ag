import logging
from datetime import datetime

from sqlalchemy import update, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM

logger = logging.getLogger(__name__)


async def update_starts_at_in_shifts(session: AsyncSession, user_tg_id: int, start_at: datetime | None = None,
                                     end_at: datetime | None = None):
    stmt = select(ShiftsORM).options(
        joinedload(ShiftsORM.page_interval).options(
            selectinload(PagesIntervalsORM.user).joinedload(UsersORM.tgs),
            selectinload(PagesIntervalsORM.page).selectinload(PagesORM.model)))
    if start_at is not None:
        stmt = stmt.filter(
            UsersORM.tgs.any(user_tg_id=user_tg_id),
            ShiftsORM.date_shift == start_at.date()
        )
    else:
        stmt = stmt.filter(
            UsersORM.tgs.any(user_tg_id=user_tg_id),
            ShiftsORM.date_shift == end_at.date()
        )
    result: Result = await session.execute(stmt)
    shifts = result.scalars().all()
    shift_ids: list[int] = [shift.id for shift in shifts]
    await session.execute(
        update(ShiftsORM).where(ShiftsORM.id.in_(shift_ids)).values(start_at=start_at)
    )
    await session.commit()

    return shifts
