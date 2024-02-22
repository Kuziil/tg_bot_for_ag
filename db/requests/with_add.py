import logging
from datetime import datetime, timezone, timedelta
import zoneinfo

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
    AgenciesModelsORM,
    AgenciesUsersORM,
    IntervalsORM,
    ModelsORM,
    PagesIntervalsORM,
    PagesORM,
    TgsORM,
    UsersORM,
)

logger = logging.getLogger(__name__)


async def add_page(
    session: AsyncSession,
    model_id: int,
    vip: bool,
    sales_commission: int,
    work_same_time: int = 1,
    page_link: str | None = None,
    senior_id: int | None = None,
) -> None:
    page = PagesORM(
        model_id=model_id,
        vip=vip,
        sales_commission=sales_commission,
        work_same_time=work_same_time,
        page_link=page_link,
        senior_id=senior_id,
    )
    session.add(page)
    await session.commit()


async def add_model(
    session: AsyncSession,
    agency_id: int,
    model_title: str,
    model_description: str | None = None,
):
    model = ModelsORM(
        title=model_title,
        description=model_description,
    )
    session.add(model)
    await session.commit()

    agency_model = AgenciesModelsORM(
        agency_id=agency_id,
        model_id=model.id,
    )
    session.add(agency_model)
    await session.commit()


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


async def add_page_interval(
    session: AsyncSession,
    page_id: int,
    interval_id: int,
) -> None:
    page_interval = PagesIntervalsORM(
        page_id=page_id,
        interval_id=interval_id,
    )
    session.add(page_interval)
    await session.commit()


async def add_interval(
    session: AsyncSession,
):
    start_at = datetime(
        year=1970,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
        microsecond=1,
        tzinfo=zoneinfo.ZoneInfo("Asia/Novosibirsk"),
    )
    logger.debug(start_at)

    start_at = start_at.astimezone(tz=zoneinfo.ZoneInfo("America/Los_Angeles"))

    logger.debug(start_at)
    end_at = datetime(
        year=1970,
        month=1,
        day=1,
        hour=1,
        minute=1,
        second=1,
        microsecond=1,
        tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles"),
    ) + timedelta(minutes=1)
    logger.debug(end_at)
    interval = IntervalsORM(
        start_at=start_at,
        end_at=end_at,
    )
    session.add(interval)
    await session.commit()


# async def add_interval(
#     session: AsyncSession,
# ):
#     interval = IntervalsORM(
#         start_at=datetime.now(timezone.utc).replace(
#             tzinfo=zoneinfo.ZoneInfo("America/Los_Angeles")
#         ),
#         end_at=datetime.now(tz=zoneinfo.ZoneInfo("America/Los_Angeles"))
#         + timedelta(minutes=1),
#     )
#     session.add(interval)
#     await session.commit()
