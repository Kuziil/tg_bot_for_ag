from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PagesORM, PagesIntervalsORM, PagesUsersORM, UsersORM


async def get_pages_available_to_user(
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
