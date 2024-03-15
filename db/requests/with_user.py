import logging

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql import false

from db.models import AgenciesUsersORM, TgsORM, UsersORM, PagesIntervalsORM, ShiftsORM, EarningsORM, RolesORM

logger = logging.getLogger(__name__)


# async def is_user_in_agency(
#         session: AsyncSession,
#         user_tg_id: int,
#         agency_id: int,
# ) -> bool:
#     stmt = (
#         select(AgenciesUsersORM)
#         .join(
#             TgsORM,
#             AgenciesUsersORM.user_id == TgsORM.user_id,
#         )
#         .filter(
#             TgsORM.user_tg_id == user_tg_id,
#             AgenciesUsersORM.agency_id == agency_id,
#         )
#     )
#     result: Result = await session.execute(stmt)
#     agency_user: AgenciesUsersORM = result.scalar_one_or_none()
#     return bool(agency_user)


async def check_user_in_agency_and_get(
        session: AsyncSession,
        user_tg_id: int,
        agency_id: int,
) -> UsersORM | None:
    stmt = select(
        UsersORM
    ).options(
        selectinload(UsersORM.tgs),
        joinedload(UsersORM.role).selectinload(RolesORM.permissions),
        joinedload(UsersORM.agencies_details)
    ).filter(
        UsersORM.tgs.any(user_tg_id=user_tg_id),
        UsersORM.agencies_details.any(agency_id=agency_id)
    )
    result: Result = await session.execute(stmt)
    user: UsersORM = result.scalar()
    return user


async def get_all_users_in_agency(
        session: AsyncSession,
        agency_id: int,
) -> list[UsersORM]:
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


async def get_user_and_available_pages_intervals_by_tg_id(
        session: AsyncSession,
        user_tg_id: int,
) -> UsersORM:
    # нужна проверка на скорость и поиграться с последовательностью
    result: Result = await session.execute(
        select(UsersORM)
        .join(UsersORM.tgs)
        .options(
            selectinload(UsersORM.tgs),
            selectinload(UsersORM.pages_intervals).joinedload(
                PagesIntervalsORM.interval
            ),
            selectinload(UsersORM.pages_intervals).joinedload(
                PagesIntervalsORM.page),
        )
        .where(TgsORM.user_tg_id == user_tg_id)
    )
    user: UsersORM = result.scalar()
    return user


async def get_user_pages_shifts_earnings(
        session: AsyncSession,
        user_tg_id: int,
):
    result: Result = await session.execute(
        select(UsersORM).options(
            selectinload(UsersORM.tgs),
            selectinload(UsersORM.pages_intervals).options(
                joinedload(PagesIntervalsORM.page),
                selectinload(PagesIntervalsORM.shifts).selectinload(
                    ShiftsORM.earnings.and_(EarningsORM.confirm == false())
                )
            )
        )
        .filter(
            UsersORM.tgs.any(user_tg_id=user_tg_id),
        )
    )
    user: UsersORM = result.scalar()
    return user
