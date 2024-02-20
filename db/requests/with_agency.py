from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import AgenciesORM


async def get_agency(session: AsyncSession, agency_id: int):
    stm = select(AgenciesORM).where(AgenciesORM.id == agency_id)
    return await session.scalar(stm)


async def get_agency_bot_id(session: AsyncSession, agency_id: int):
    stmt = select(AgenciesORM.test_tg_bot).where(AgenciesORM.id == agency_id)
    return await session.scalar(stmt)
