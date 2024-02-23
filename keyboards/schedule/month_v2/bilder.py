import datetime as dt
from calendar import monthcalendar
from zoneinfo import ZoneInfo
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests.with_page import (
    get_pages_with_inter_users_tgs_by_user_tg_id,
)
from db.models import (
    PagesORM,
    PagesIntervalsORM,
    IntervalsORM,
    UsersORM,
    TgsORM,
    ModelsORM,
)

logger = logging.getLogger(__name__)


async def convert_interval_to_str(
    defult_tz: ZoneInfo,
    interval: IntervalsORM,
):
    interval_list: list[dt.datetime] = [interval.start_at, interval.end_at]
    for i in range(len(interval_list)):
        interval_list[i] = interval_list[i].astimezone(defult_tz).strftime("%H:%M")
    interval_str: str = f"{interval_list[0]}-{interval_list[1]}"
    return interval_str


async def create_month_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    defult_tz: ZoneInfo,
    current_page: PagesORM | None = None,
    current_year: int = 1,
    current_month: int = 1,
    current_day: int = 1,
):
    pages: list[PagesORM] = await get_pages_with_inter_users_tgs_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
    )
    month_calendar: list[list[int]] = monthcalendar(year=1, month=1)

    if not current_page:
        page: PagesORM = pages[0]
    else:
        page: PagesORM = current_page

    model: ModelsORM = page.model
    pages_intervals: list[PagesIntervalsORM] = page.intervals_details
    interval: IntervalsORM = pages_intervals[0].interval
    interval_str: str = await convert_interval_to_str(
        defult_tz=defult_tz,
        interval=interval,
    )

    kb_builder = InlineKeyboardBuilder()

    # row test
    kb_builder.row(
        InlineKeyboardButton(
            text=f"{interval_str}",
            callback_data="test",
        )
    )
    return kb_builder.as_markup()
