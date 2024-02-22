import datetime as dt
from calendar import monthcalendar
from zoneinfo import ZoneInfo
from random import randint

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


async def create_mounth_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    defult_tz: ZoneInfo,
    current_page: PagesORM | None = None,
) -> InlineKeyboardMarkup:
    pages: list[PagesORM] = await get_pages_with_inter_users_tgs_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
    )
    if not current_page:
        page: PagesORM = pages[0]
        model: ModelsORM = page.model
        pages_intervals: list[PagesIntervalsORM] = page.intervals_details
        interval: IntervalsORM = pages_intervals[0].interval
        interval_start_at: dt.datetime = interval.start_at

    kb_builder = InlineKeyboardBuilder()

    # row test
    kb_builder.row(
        InlineKeyboardButton(
            text=f"{interval_start_at.astimezone(defult_tz)}",
            callback_data="test",
        )
    )
    return kb_builder.as_markup()
