from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message

from db.models import Agencies, Users


async def get_agency_bot_id(session: AsyncSession, agency_id: int):
    stmt = select(Agencies.test_tg_bot).where(Agencies.agency_id == agency_id)
    return await session.scalar(stmt)


# async def add_user(session: AsyncSession, name: str):
#     agency = Agencies(title=name)
#     session.add(agency)
#     await session.commit()

async def add_user(session: AsyncSession, name: str, emoji: str):
    user = Users(name=name, emoji=emoji)
    session.add(user)
    await session.commit()


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select()
    return await session.scalar(stmt)
