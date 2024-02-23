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
from keyboards.schedule.month_v2.classes_callback_data import IntervalCallbackData

logger = logging.getLogger(__name__)


async def convert_interval_to_str(
    defult_tz: ZoneInfo,
    interval: IntervalsORM,
) -> list[str]:
    interval_list: list[dt.datetime] = [interval.start_at, interval.end_at]
    for i in range(len(interval_list)):
        interval_list[i] = interval_list[i].astimezone(defult_tz).strftime("%H:%M")
    return interval_list


async def create_month_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    defult_tz: ZoneInfo,
    current_page: PagesORM | None = None,
    current_year: int = 1,
    current_month: int = 1,
    current_day: int = 1,
    current_start_at: str | None = None,
    current_end_at: str | None = None,
):
    pages: list[PagesORM] = await get_pages_with_inter_users_tgs_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
    )
    kb_builder = InlineKeyboardBuilder()
    month_calendar: list[list[int]] = monthcalendar(year=1, month=1)

    if not current_page:
        page: PagesORM = pages[0]
    else:
        page: PagesORM = current_page

    model: ModelsORM = page.model
    pages_intervals: list[PagesIntervalsORM] = page.intervals_details
    current_interval_list: list[str] = [current_start_at, current_end_at]

    if not current_start_at or not current_end_at:
        for page_interval in pages_intervals:
            user: UsersORM = page_interval.user
            if user:
                tgs = user.tgs
                for tg in tgs:
                    if tg.user_tg_id == user_tg_id:
                        interval: IntervalsORM = page_interval.interval
                        interval_list: str = await convert_interval_to_str(
                            defult_tz=defult_tz,
                            interval=interval,
                        )
                        break
    else:
        for interval in pages_intervals:
            interval_list: str = await convert_interval_to_str(
                defult_tz=defult_tz,
                interval=interval,
            )

    # row test
    kb_builder.row(
        # InlineKeyboardButton(
        #     text=f"<<<",
        #     callback_data=IntervalCallbackData(
        #         start_at=None,
        #         end_at=None,
        #     ).pack(),
        # ),
        InlineKeyboardButton(
            text=f"{interval_list[0]}-{interval_list[1]}",
            callback_data=IntervalCallbackData(
                start_at=interval_list[0],
                end_at=interval_list[1],
            ).pack(),
        ),
        # InlineKeyboardButton(
        #     text=f">>>",
        #     callback_data=IntervalCallbackData(
        #         start_at=None,
        #         end_at=None,
        #     ).pack(),
        # ),
    )
    return kb_builder.as_markup()
