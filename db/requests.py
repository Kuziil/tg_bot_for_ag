from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Agencies


async def add_new_user(session: AsyncSession, titel: str, tg_bot_id: int, test_tg_bot: int):
    async with session.begin():
        new_user = Agencies(titel=titel, tg_bot_id=tg_bot_id,
                            test_tg_bot=test_tg_bot)
        session.add(new_user)
        await session.commit()


async def test_connection(session: AsyncSession):
    """
    Проверка соединения с СУБД
    :param session: объект AsyncSession
    """
    stmt = select(1)
    return await session.scalar(stmt)
