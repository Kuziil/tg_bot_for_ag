from datetime import datetime, time
from calendar import monthcalendar
from zoneinfo import ZoneInfo
from random import randint

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests.with_page import (
    get_pages_with_inter_users_tgs_by_user_tg_id,
)
from db.models import PagesORM, PagesIntervalsORM, IntervalsORM, UsersORM, TgsORM


async def create_week_shudle(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    deafult_tz: ZoneInfo,
    # nyc = ZoneInfo("America/New_York")
    # localized = datetime(2022, 6, 4, tzinfo=nyc)
    current_page: PagesORM | None = None,
) -> InlineKeyboardMarkup:
    pages: list[PagesORM] = await get_pages_with_inter_users_tgs_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
    )
    kb_builder = InlineKeyboardBuilder()
    row_1: list[InlineKeyboardButton] = []
    row_1.append(
        InlineKeyboardButton(
            text=f"+3",
            callback_data=f"{randint(100,1000)}",
        )
    )
    if not current_page:
        page = pages[0]
    user_not_found: bool = True
    pages_intervals: list[PagesIntervalsORM] = page.intervals_details
    for page_interval in pages_intervals:
        interval: IntervalsORM = page_interval.interval
        start_at: time = datetime.combine(
            datetime.min,
            interval.start_at,
        ).astimezone(deafult_tz)
        end_at: time = datetime.combine(
            datetime.min,
            interval.start_at,
        ).astimezone(deafult_tz)
        str_start_at: str = f"{start_at.hour}:{start_at.minute}"
        str_end_at: str = f"{end_at.hour}:{end_at.minute}"
        str_interval: str = f"{str_start_at}-{str_end_at}"
        user: UsersORM = page_interval.user
        if user_not_found:
            if user:
                tgs: list[TgsORM] = user.tgs
                for tg in tgs:
                    if tg.user_tg_id == user_tg_id:
                        user_not_found = False
                        str_interval = f"[{str_interval}]"
        row_1.append(
            InlineKeyboardButton(
                text=str_interval,
                callback_data=f"{randint(100,1000)}",
            )
        )
    kb_builder.row(*row_1)

    # mounth_calendar: list[list[int]] = monthcalendar(
    #     date_utc_now.year,
    #     date_utc_now.month,
    # )

    # row 2 - 8

    # row 9
    kb_builder.row(
        InlineKeyboardButton(
            text=f"<<",
            callback_data="back",
        ),
        InlineKeyboardButton(
            text=f"page",
            callback_data="ppage",
        ),
        InlineKeyboardButton(
            text=f">>",
            callback_data="forward",
        ),
    )

    return kb_builder.as_markup()
