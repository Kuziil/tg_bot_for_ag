from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PagesORM, PagesIntervalsORM, PagesUsersORM, UsersORM


async def get_all_pages_with_intervals_and_with_users_tgs(
    session: AsyncSession,
    user_id: int,
):
    result: Result = await session.execute(
        select(PagesORM).options(
            selectinload(PagesORM.intervals_details).joinedload(
                PagesIntervalsORM.interval
            ),
            selectinload(PagesORM.users_details)
            .joinedload(PagesUsersORM.user)
            .selectinload(UsersORM.tgs),
        )
    )
    pages: list[PagesORM] = result.scalars().all()
    return pages
