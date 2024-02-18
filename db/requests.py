import logging

from sqlalchemy import select, or_
from sqlalchemy.engine import Result, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from db.models import AgenciesORM, UsersORM, TgsORM, AgenciesUsersORM
from sqlalchemy.orm import joinedload


# Инициализируем логгер
logger = logging.getLogger(__name__)


async def get_agency_bot_id(session: AsyncSession, agency_id: int):
    stmt = select(AgenciesORM.test_tg_bot).where(AgenciesORM.id == agency_id)
    return await session.scalar(stmt)


async def get_agency(session: AsyncSession, agency_id: int):
    stm = select(AgenciesORM).where(AgenciesORM.id == agency_id)
    return await session.scalar(stm)


async def add_user(
    session: AsyncSession,
    username: str,
    emoji: str,
    user_tg_id: int,
    agency_id: int,
):
    user = UsersORM(
        username=username,
        emoji=emoji,
    )
    session.add(user)
    await session.commit()

    user_tg_id = TgsORM(
        user_tg_id=user_tg_id,
        user_id=user.id,
    )
    session.add(user_tg_id)
    await session.commit()

    agency_user = AgenciesUsersORM(
        agency_id=agency_id,
        user_id=user.id,
    )
    session.add(agency_user)
    await session.commit()


async def check_for_bot_id_in_db(
    session: AsyncSession,
    bot_id: int,
    agency_id: int | None = None,
):
    try:
        if agency_id:
            stmt = select(AgenciesORM).where(
                AgenciesORM.id == agency_id,
            )
        else:
            stmt = select(AgenciesORM).where(
                or_(
                    AgenciesORM.main_tg_bot == bot_id,
                    AgenciesORM.test_tg_bot == bot_id,
                )
            )

        result: Result = await session.execute(stmt)

        agency: AgenciesORM = result.scalar_one()

        if agency.main_tg_bot == bot_id:
            logger.info("The MAIN bot has been started")
            return agency.id, agency.title
        elif agency.test_tg_bot == bot_id:
            logger.info("The TEST bot has been started")
            return agency.id, agency.title

    except NoResultFound:
        raise ValueError("Bot ID not found in the database")


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select()
    return await session.scalar(stmt)


async def is_user_in_agency(session: AsyncSession, user_tg_id: int, agency_id: int):
    stmt = (
        select(AgenciesUsersORM)
        .join(TgsORM, AgenciesUsersORM.user_id == TgsORM.user_id)
        .filter(
            TgsORM.user_tg_id == user_tg_id, AgenciesUsersORM.agency_id == agency_id
        )
    )
    result: Result = await session.execute(stmt)
    agency_user: AgenciesUsersORM = result.scalar_one_or_none()
    return bool(agency_user)


async def get_all_users_in_agency(session: AsyncSession, agency_id: int):
    stmt = (
        select(UsersORM)
        .join(UsersORM.agencies_details)
        .options(selectinload(UsersORM.agencies_details))
        .filter(AgenciesUsersORM.agency_id == agency_id)
        .order_by(UsersORM.id)
    )
    result: Result = await session.execute(stmt)
    users: list[UsersORM] = result.scalars().all()
    logger.debug(users)
    return users


async def get_all_emojis_in_agency(
    session: AsyncSession, agency_id: int
) -> set[str] | None:
    users = await get_all_users_in_agency(session=session, agency_id=agency_id)
    emojis: set[str] = set()
    for user in users:
        emojis.add(user.emoji)
    return emojis


async def is_busy_emoji_in_agency(session: AsyncSession, emoji: str, agency_id: int):
    emojis = await get_all_emojis_in_agency(session=session, agency_id=agency_id)
    return emoji in emojis
