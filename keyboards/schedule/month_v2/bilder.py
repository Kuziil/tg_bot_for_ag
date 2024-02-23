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
) -> dict[str, str]:
    # interval_list: dict[strdt.datetime] = [interval.start_at, interval.end_at]
    dict_current_interval: dict[str, str] = {}
    start_at: dt.datetime = interval.start_at.astimezone(defult_tz)
    end_at: dt.datetime = interval.end_at.astimezone(defult_tz)
    dict_current_interval["start_at"] = start_at.strftime("%H:%M")
    dict_current_interval["end_at"] = end_at.strftime("%H:%M")
    return dict_current_interval


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
    dict_intervals: dict[str, dict[str, str]] = {}

    if not current_start_at or not current_end_at:
        for page_interval in pages_intervals:
            user: UsersORM = page_interval.user
            interval: IntervalsORM = page_interval.interval
            if "current" in dict_intervals:
                dict_intervals["after"] = await convert_interval_to_str(
                    defult_tz=defult_tz,
                    interval=interval,
                )
                break
            if user:
                tgs = user.tgs
                logger.debug(f"tgs: {user}")
                for tg in tgs:
                    if tg.user_tg_id == user_tg_id:
                        dict_intervals["current"] = await convert_interval_to_str(
                            defult_tz=defult_tz,
                            interval=interval,
                        )
                        break
            if "current" not in dict_intervals:
                dict_intervals["before"] = await convert_interval_to_str(
                    defult_tz=defult_tz,
                    interval=interval,
                )
        if "before" not in dict_intervals:
            dict_intervals["before"] = await convert_interval_to_str(
                defult_tz=defult_tz,
                interval=interval,
            )

    else:
        pass

    # row test
    kb_builder.row(
        InlineKeyboardButton(
            text=f"<<<",
            callback_data=IntervalCallbackData(
                start_at=dict_intervals["before"]["start_at"],
                end_at=dict_intervals["before"]["end_at"],
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f'{dict_intervals["current"]["start_at"]}-{dict_intervals["current"]["end_at"]}',
            callback_data=IntervalCallbackData(
                start_at=dict_intervals["current"]["start_at"],
                end_at=dict_intervals["current"]["end_at"],
            ).pack(),
        ),
        InlineKeyboardButton(
            text=f">>>",
            callback_data=IntervalCallbackData(
                start_at=dict_intervals["after"]["start_at"],
                end_at=dict_intervals["after"]["end_at"],
            ).pack(),
        ),
    )
    return kb_builder.as_markup()
