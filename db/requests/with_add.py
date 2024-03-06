import logging
import datetime as dt
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import (
    AgenciesPagesORM,
    AgenciesUsersORM,
    IntervalsORM,
    ModelsORM,
    PagesIntervalsORM,
    PagesORM,
    TgsORM,
    UsersORM,
    ShiftsORM,
)

logger = logging.getLogger(__name__)


async def add_shift(
    session: AsyncSession,
    date_shift: dt.date,
    page_interval_id: int,
    replacement_id: int | None = None,
):
    shift = ShiftsORM(
        date_shift=date_shift,
        page_interval_id=page_interval_id,
        replacement_id=replacement_id,
    )
    session.add(shift)
    await session.commit()


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

    agency_model = AgenciesPagesORM(
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

    tgs: TgsORM = TgsORM(
        user_tg_id=user_tg_id,
        user_id=user.id,
    )
    session.add(tgs)
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
    default_tz: ZoneInfo,
    start_at: dt.time,
    end_at: dt.time,
):
    start_at_1 = dt.datetime(
        year=1970,
        month=1,
        day=1,
        hour=start_at.hour,
        minute=start_at.minute,
        tzinfo=default_tz,
    )
    end_at_1 = dt.datetime(
        year=1970,
        month=1,
        day=1,
        hour=end_at.hour,
        minute=end_at.minute,
        tzinfo=default_tz,
    )
    interval = IntervalsORM(
        start_at=start_at_1,
        end_at=end_at_1,
    )
    session.add(interval)
    await session.commit()


async def add_shifts(
    session: AsyncSession,
    st_shifts: list[dict[str, str]],
):
    shifts = []
    for st_shift in st_shifts:
        shifts.append(
            ShiftsORM(
                date_shift=dt.datetime(
                    year=st_shift["year"],
                    month=st_shift["month"],
                    day=st_shift["day"],
                ),
                page_interval_id=st_shift["page_interval_id"],
            )
        )

    session.add_all(shifts)
    await session.commit()
