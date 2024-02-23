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


async def process_intervals(
    current_start_at: str,
    current_end_at: str,
    defult_tz: ZoneInfo,
    pages_intervals: list[PagesIntervalsORM],
    user_tg_id: int,
) -> dict[str, dict[str, str]]:
    dict_intervals: dict[str, dict[str, str]] = {}
    current_interval_dict: dict[str, str] = {
        "start_at": current_start_at,
        "end_at": current_end_at,
    }

    current: int | None = None
    interval_dict_list: list[dict[str, str]] = []
    interval_for_user: int | None = None
    for key, page_interval in enumerate(pages_intervals):
        interval: IntervalsORM = page_interval.interval
        interval_dict_list.append(
            await convert_interval_to_str(
                defult_tz=defult_tz,
                interval=interval,
            )
        )
        if interval_for_user is None:
            user: UsersORM = page_interval.user
            tgs = user.tgs
            for tg in tgs:
                if tg.user_tg_id == user_tg_id:
                    interval_for_user = key
                    if not current_start_at or not current_end_at:
                        current = key
                    break
        if interval_dict_list[key] == current_interval_dict:
            current = key
    dict_intervals["current"] = interval_dict_list[current]
    if current == 0:
        dict_intervals["before"] = interval_dict_list[-1]
        dict_intervals["after"] = interval_dict_list[current + 1]
    elif current == len(pages_intervals) - 1:
        dict_intervals["before"] = interval_dict_list[current - 1]
        dict_intervals["after"] = interval_dict_list[0]
    else:
        dict_intervals["before"] = interval_dict_list[current - 1]
        dict_intervals["after"] = interval_dict_list[current + 1]

    return dict_intervals


async def process_page():
    pass


async def create_month_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    defult_tz: ZoneInfo,
    current_page: str | None = None,
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
        model: ModelsORM = page.model
        model_name: str = model.title
        work_the_same_time: int = page.work_same_time
    else:
        pass

    model: ModelsORM = page.model
    pages_intervals: list[PagesIntervalsORM] = page.intervals_details
    pages_intervals = sorted(pages_intervals, key=lambda x: x.interval.start_at)

    dict_intervals = await process_intervals(
        current_start_at=current_start_at,
        current_end_at=current_end_at,
        defult_tz=defult_tz,
        pages_intervals=pages_intervals,
        user_tg_id=user_tg_id,
    )

    # row test
    kb_builder.row(
        InlineKeyboardButton(
            text="7",
            callback_data="test",
        )
    )

    # row interval
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
