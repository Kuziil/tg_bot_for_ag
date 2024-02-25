import datetime as dt
from calendar import monthcalendar, monthrange
from typing import Any
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
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthShudleCallbackData,
)

logger = logging.getLogger(__name__)


async def in_circle(
    values: list[Any],
    current: int,
):
    dict_position: dict[str, Any] = {}
    dict_position["current"] = values[current]
    len_values: int = len(values)
    if len_values == 1:
        return dict_position
    if current == 0:
        dict_position["before"] = values[-1]
        dict_position["after"] = values[current + 1]
    elif current == len_values - 1:
        dict_position["before"] = values[current - 1]
        dict_position["after"] = values[0]
    else:
        dict_position["before"] = values[current - 1]
        dict_position["after"] = values[current + 1]
    return dict_position


async def process_page(
    pages: list[PagesORM],
    current_page_id: int,
) -> dict[str, PagesORM]:
    current: int = 0
    for key, page in enumerate(pages):
        page: PagesORM = page
        if page.id == current_page_id:
            current = key
            break
    return await in_circle(values=pages, current=current)


async def convert_interval_to_str(
    defult_tz: ZoneInfo,
    interval: IntervalsORM,
) -> str:
    start_at: str = interval.start_at.astimezone(defult_tz).strftime("%H:%M")
    end_at: str = interval.end_at.astimezone(defult_tz).strftime("%H:%M")
    return f"{start_at}-{end_at}"


async def process_intervals_and_lineups(
    current_interval_id: int | None,
    current_lineup: int | None,  # lineup
    pages_intervals: list[PagesIntervalsORM],
    user_tg_id: int,
) -> tuple[dict[str, IntervalsORM], dict[str, int]]:
    intervals: list[IntervalsORM] = []
    lineups: list[int] = []  # lineup
    current_interval_key: int | None = None
    current_lineup_key: int | None = None  # lineup
    for key, page_interval in enumerate(pages_intervals):
        interval: IntervalsORM = page_interval.interval
        intervals.append(interval)
        lineup: int = page_interval.lineup  # lineup
        if lineup not in lineups:  # lineup
            lineups.append(lineup)  # lineup
        if current_interval_id is None and current_lineup is None:
            user: UsersORM = page_interval.user
            if user is not None:
                tgs: list[TgsORM] = user.tgs
                for tg in tgs:
                    if tg.user_tg_id == user_tg_id:
                        current_interval_key = key
                        current_lineup = lineup  # lineup
        else:
            if interval.id == current_interval_id:
                current_interval_key = key
    lineups.sort()
    current_lineup_key = current_lineup - 1  # lineup
    dict_intervals: dict[str, IntervalsORM] = await in_circle(
        values=intervals,
        current=current_interval_key,
    )
    dict_lineups: dict[str, int] = await in_circle(
        values=lineups,
        current=current_lineup_key,
    )  # lineup
    return dict_intervals, dict_lineups


async def create_row_month_year(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
):
    before_month_year_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f"<",
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["before"].day,
            month=dict_datetimes["before"].month,
            year=dict_datetimes["before"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    current_month_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f'{dict_datetimes["current"].strftime("%B")}',
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    current_year_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f'{dict_datetimes["current"].year}',
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    after_month_year_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f">",
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["after"].day,
            month=dict_datetimes["after"].month,
            year=dict_datetimes["after"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    return (
        before_month_year_ikb,
        current_month_ikb,
        current_year_ikb,
        after_month_year_ikb,
    )


async def create_row_pages(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
):
    current_page_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=dict_pages["current"].model.title,
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    current_page_type_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=dict_pages["current"].type_in_agency,
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    if "before" in dict_pages and "after" in dict_pages:
        before_page_ikb: InlineKeyboardButton = InlineKeyboardButton(
            text="<<",
            callback_data=MonthShudleCallbackData(
                day=dict_datetimes["current"].day,
                month=dict_datetimes["current"].month,
                year=dict_datetimes["current"].year,
                page_id=dict_pages["before"].id,
                lineup=dict_lineups["current"],
                interval_id=dict_intervals["current"].id,
            ).pack(),
        )
        after_page_ikb: InlineKeyboardButton = InlineKeyboardButton(
            text=">>",
            callback_data=MonthShudleCallbackData(
                day=dict_datetimes["current"].day,
                month=dict_datetimes["current"].month,
                year=dict_datetimes["current"].year,
                page_id=dict_pages["after"].id,
                lineup=dict_lineups["current"],
                interval_id=dict_intervals["current"].id,
            ).pack(),
        )
        return before_page_ikb, current_page_ikb, current_page_type_ikb, after_page_ikb
    else:
        return current_page_ikb, current_page_type_ikb


async def create_row_inervals(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
    defult_tz: ZoneInfo,
):
    before_interval_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f"<<<",
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["before"].id,
        ).pack(),
    )
    current_interval_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f'{await convert_interval_to_str(interval=dict_intervals["current"], defult_tz=defult_tz,)}',
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    after_interval_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f">>>",
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["after"].id,
        ).pack(),
    )

    return before_interval_ikb, current_interval_ikb, after_interval_ikb


async def create_row_lineups(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
):
    before_lineup_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f"<<<",
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["before"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    current_lineup_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f'{dict_lineups["current"]}',
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["current"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    after_lineup_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f">>>",
        callback_data=MonthShudleCallbackData(
            day=dict_datetimes["current"].day,
            month=dict_datetimes["current"].month,
            year=dict_datetimes["current"].year,
            page_id=dict_pages["current"].id,
            lineup=dict_lineups["after"],
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    return before_lineup_ikb, current_lineup_ikb, after_lineup_ikb


async def create_month_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    defult_tz: ZoneInfo,
    current_page_id: int | None = None,
    current_year: int | None = None,
    current_month: int | None = None,
    current_day: int | None = None,
    current_interval_id: int | None = None,
    current_lineup: int | None = None,
):
    pages: list[PagesORM] = await get_pages_with_inter_users_tgs_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
    )
    kb_builder = InlineKeyboardBuilder()
    dict_datetimes: dict[str, dt.datetime] = {}
    if current_year is None or current_month is None or current_day is None:
        current_datetime: dt.datetime = dt.datetime.now(tz=defult_tz)
    else:
        current_datetime: dt.datetime = dt.datetime(
            year=current_year,
            month=current_month,
            day=current_day,
            tzinfo=defult_tz,
        )
    dict_datetimes["current"] = current_datetime
    timedelta_of_days_for_current_month: dt.timedelta = dt.timedelta(
        days=monthrange(
            year=dict_datetimes["current"].year,
            month=dict_datetimes["current"].month,
        )[1]
    )
    dict_datetimes["before"] = (
        dict_datetimes["current"] - timedelta_of_days_for_current_month
    )
    dict_datetimes["after"] = (
        dict_datetimes["current"] + timedelta_of_days_for_current_month
    )
    month_calendar: list[list[int]] = monthcalendar(
        year=dict_datetimes["current"].year,
        month=dict_datetimes["current"].month,
    )
    pages = sorted(pages, key=lambda x: (x.model.title, x.type_in_agency))
    # for page_t in pages:
    #     logger.debug(f"{page_t}")
    #     logger.debug(f"    {page_t.model}")
    #     for page_interval_t in page_t.intervals_details:
    #         logger.debug(f"    {page_interval_t}")
    #         logger.debug(f"    {page_interval_t.interval}")
    #         logger.debug(f"    {page_interval_t.page}")
    #         logger.debug(f"    {page_interval_t.user}")
    #         if page_interval_t.user is not None:
    #             for tgs_t in page_interval_t.user.tgs:
    #                 logger.debug(f"        {tgs_t}")
    #         else:
    #             logger.debug(f"            None")
    dict_pages: dict[str, PagesORM] = await process_page(
        pages=pages,
        current_page_id=current_page_id,
    )

    page: PagesORM = dict_pages["current"]
    pages_intervals: list[PagesIntervalsORM] = sorted(
        page.intervals_details,
        key=lambda x: x.interval.start_at,
    )

    dict_intervals_and_lineups = await process_intervals_and_lineups(
        current_interval_id=current_interval_id,
        current_lineup=current_lineup,
        pages_intervals=pages_intervals,
        user_tg_id=user_tg_id,
    )

    dict_intervals: dict[str, IntervalsORM] = dict_intervals_and_lineups[0]
    dict_lineups: dict[str, int] = dict_intervals_and_lineups[1]

    # row month_year
    kb_builder.row(
        *await create_row_month_year(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
        )
    )

    # row lineup
    if "before" in dict_lineups and "after" in dict_lineups:
        kb_builder.row(
            *await create_row_lineups(
                dict_datetimes=dict_datetimes,
                dict_pages=dict_pages,
                dict_lineups=dict_lineups,
                dict_intervals=dict_intervals,
            )
        )
    # row page
    kb_builder.row(
        *await create_row_pages(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
        )
    )
    # row interval
    kb_builder.row(
        *await create_row_inervals(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
            defult_tz=defult_tz,
        )
    )

    return kb_builder.as_markup()
