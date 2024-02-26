from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import PagesORM, PagesIntervalsORM, UsersORM, TgsORM


async def get_pages_with_inter_users_tgs_by_user_tg_id(
    session: AsyncSession,
    user_tg_id: int,
):
    result: Result = await session.execute(
        select(PagesORM)
        .join(PagesIntervalsORM, PagesORM.id == PagesIntervalsORM.page_id)
        .join(UsersORM, PagesIntervalsORM.user_id == UsersORM.id)
        .join(TgsORM, UsersORM.id == TgsORM.user_id)
        .options(
            joinedload(PagesORM.model),
            selectinload(PagesORM.intervals_details).options(
                joinedload(PagesIntervalsORM.interval),
                joinedload(PagesIntervalsORM.user).selectinload(UsersORM.tgs),
            ),
        )
        .where(TgsORM.user_tg_id == user_tg_id)
    )
    pages: list[PagesORM] = result.scalars().all()
    return pages
