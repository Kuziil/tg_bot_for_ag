from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import TgsORM, UsersORM
from db.requests.with_user import get_all_users_in_agency


async def get_all_emojis_in_agency(
        session: AsyncSession, agency_id: int
) -> set[str] | None:
    users = await get_all_users_in_agency(
        session=session,
        agency_id=agency_id,
    )
    emojis: set[str] = set()
    for user in users:
        emojis.add(user.emoji)
    return emojis


async def is_busy_emoji_in_agency(
        session: AsyncSession,
        emoji: str,
        agency_id: int,
):
    emojis = await get_all_emojis_in_agency(
        session=session,
        agency_id=agency_id,
    )
    return emoji in emojis


async def get_str_emojis_in_agency(
        session: AsyncSession,
        agency_id: int,
) -> str:
    emojis = await get_all_emojis_in_agency(
        session=session,
        agency_id=agency_id,
    )
    return " ".join(emojis)


async def get_emoji_by_user_tg_id(
        session: AsyncSession,
        user_tg_id: int,
) -> str:
    stmt = (
        select(UsersORM)
        .options(selectinload(UsersORM.tgs))
        .filter(TgsORM.user_tg_id == user_tg_id)
    )
    result: Result = await session.execute(stmt)
    user: UsersORM = result.scalar_one()
    return user.emoji
