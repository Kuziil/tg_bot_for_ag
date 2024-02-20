import logging

from sqlalchemy import or_, select
from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import AgenciesORM

logger = logging.getLogger(__name__)


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select()
    return await session.scalar(stmt)


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
