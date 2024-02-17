import logging

from sqlalchemy import select, or_
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from db.models import AgenciesORM, UsersORM, TgsORM, AgenciesUsersORM


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
    return bool(result.scalars().first())
