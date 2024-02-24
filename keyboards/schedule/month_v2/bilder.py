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
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthShudleCallbackData,
)

logger = logging.getLogger(__name__)


async def process_page(
    pages: list[PagesORM],
    current_page_id: int,
) -> dict[str, PagesORM]:
    dict_pages: dict[str, PagesORM] = {}
    current: int = 0
    for key, page in enumerate(pages):
        page: PagesORM = page
        if page.id == current_page_id:
            current = key
            break
    dict_pages["current"] = pages[current]
    len_pages: int = len(pages)
    if len_pages == 1:
        return dict_pages
    if current == 0:
        dict_pages["before"] = pages[-1]
        dict_pages["after"] = pages[current + 1]
    elif current == len_pages - 1:
        dict_pages["before"] = pages[current - 1]
        dict_pages["after"] = pages[0]
    else:
        dict_pages["before"] = pages[current - 1]
        dict_pages["after"] = pages[current + 1]
    return dict_pages


async def convert_interval_to_str(
    defult_tz: ZoneInfo,
    interval: IntervalsORM,
) -> str:
    start_at: str = interval.start_at.astimezone(defult_tz).strftime("%H:%M")
    end_at: str = interval.end_at.astimezone(defult_tz).strftime("%H:%M")
    return f"{start_at}-{end_at}"


async def process_intervals_and_lineups(
    current_interval_id: int | None,
    pages_intervals: list[PagesIntervalsORM],
    user_tg_id: int,
) -> tuple[dict[str, IntervalsORM], set[int]]:
    dict_intervals: dict[str, IntervalsORM] = {}
    lineups: set[int] = set()  # lineup
    current: int | None = None
    intervals: list[IntervalsORM] = []
    for key, page_interval in enumerate(pages_intervals):
        interval: IntervalsORM = page_interval.interval
        intervals.append(interval)
        lineups.add(page_interval.lineup)  # lineup
        if current_interval_id is None:
            user: UsersORM = page_interval.user
            if user is not None:
                tgs: list[TgsORM] = user.tgs
                for tg in tgs:
                    if tg.user_tg_id == user_tg_id:
                        current = key
        else:
            if interval.id == current_interval_id:
                current = key
    dict_intervals["current"] = intervals[current]
    if current == 0:
        dict_intervals["before"] = intervals[-1]
        dict_intervals["after"] = intervals[current + 1]
    elif current == len(intervals) - 1:
        dict_intervals["before"] = intervals[current - 1]
        dict_intervals["after"] = intervals[0]
    else:
        dict_intervals["before"] = intervals[current - 1]
        dict_intervals["after"] = intervals[current + 1]
    return dict_intervals, lineups


async def create_row_pages(
    dict_pages: dict[str, PagesORM],
    dict_intervals: dict[str, IntervalsORM],
):
    current_page_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=dict_pages["current"].model.title,
        callback_data=MonthShudleCallbackData(
            page_id=dict_pages["current"].id,
            lineup=1,
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    current_page_type_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=dict_pages["current"].type_in_agency,
        callback_data=MonthShudleCallbackData(
            page_id=dict_pages["current"].id,
            lineup=1,
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    if "before" in dict_pages and "after" in dict_pages:
        before_page_ikb: InlineKeyboardButton = InlineKeyboardButton(
            text="<<",
            callback_data=MonthShudleCallbackData(
                page_id=dict_pages["before"].id,
                lineup=1,
                interval_id=dict_intervals["current"].id,
            ).pack(),
        )
        after_page_ikb: InlineKeyboardButton = InlineKeyboardButton(
            text=">>",
            callback_data=MonthShudleCallbackData(
                page_id=dict_pages["after"].id,
                lineup=1,
                interval_id=dict_intervals["current"].id,
            ).pack(),
        )
        return before_page_ikb, current_page_ikb, current_page_type_ikb, after_page_ikb
    else:
        return current_page_ikb, current_page_type_ikb


async def create_row_inervals(
    dict_pages: dict[str, PagesORM],
    dict_intervals: dict[str, IntervalsORM],
    defult_tz: ZoneInfo,
):
    before_interval_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f"<<<",
        callback_data=MonthShudleCallbackData(
            page_id=dict_pages["current"].id,
            lineup=1,
            interval_id=dict_intervals["before"].id,
        ).pack(),
    )
    current_interval_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f'{await convert_interval_to_str(interval=dict_intervals["current"], defult_tz=defult_tz,)}',
        callback_data=MonthShudleCallbackData(
            page_id=dict_pages["current"].id,
            lineup=1,
            interval_id=dict_intervals["current"].id,
        ).pack(),
    )
    after_interval_ikb: InlineKeyboardButton = InlineKeyboardButton(
        text=f">>>",
        callback_data=MonthShudleCallbackData(
            page_id=dict_pages["current"].id,
            lineup=1,
            interval_id=dict_intervals["after"].id,
        ).pack(),
    )

    return before_interval_ikb, current_interval_ikb, after_interval_ikb


async def create_month_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    defult_tz: ZoneInfo,
    current_page_id: int | None = None,
    current_year: int = 1,
    current_month: int = 1,
    current_day: int = 1,
    current_interval_id: int | None = None,
    lineup: int | None = None,
):
    pages: list[PagesORM] = await get_pages_with_inter_users_tgs_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
    )
    kb_builder = InlineKeyboardBuilder()
    month_calendar: list[list[int]] = monthcalendar(year=1, month=1)
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
    dict_intervals_and_set_lineups = await process_intervals_and_lineups(
        current_interval_id=current_interval_id,
        pages_intervals=pages_intervals,
        user_tg_id=user_tg_id,
    )
    logger.debug(type(dict_intervals_and_set_lineups))
    dict_intervals: dict[str, IntervalsORM] = dict_intervals_and_set_lineups[0]
    lineups: set[int] = dict_intervals_and_set_lineups[1]

    # row pages
    kb_builder.row(
        *await create_row_pages(
            dict_pages,
            dict_intervals,
        )
    )
    # row interval
    kb_builder.row(
        *await create_row_inervals(
            dict_pages=dict_pages,
            dict_intervals=dict_intervals,
            defult_tz=defult_tz,
        )
    )
    return kb_builder.as_markup()
