import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import update, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM

logger = logging.getLogger(__name__)


async def update_starts_at_in_shifts(session: AsyncSession, user_tg_id: int, default_tz: ZoneInfo) -> None:
    start_at = datetime.now(tz=default_tz)
    logger.debug(start_at)
    result: Result = await session.execute(
        select(ShiftsORM).options(
            joinedload(ShiftsORM.page_interval).options(
                selectinload(PagesIntervalsORM.user).joinedload(UsersORM.tgs),
                selectinload(PagesIntervalsORM.page).selectinload(PagesORM.model))).filter(
            UsersORM.tgs.any(user_tg_id=user_tg_id),
            ShiftsORM.date_shift == start_at.date()
        )
    )
    shifts = result.scalars().all()
    shift_ids: list[int] = [shift.id for shift in shifts]
    await session.execute(
        update(ShiftsORM).where(ShiftsORM.id.in_(shift_ids)).values(start_at=start_at)
    )
    await session.commit()
