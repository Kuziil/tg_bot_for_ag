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


async def create_mounth_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    deafult_tz: ZoneInfo,
    # nyc = ZoneInfo("America/New_York")
    # localized = datetime(2022, 6, 4, tzinfo=nyc)
    current_page: PagesORM | None = None,
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    # row test
    kb_builder.row(
        InlineKeyboardButton(
            text=f"test",
            callback_data="test",
        )
    )
    return kb_builder.as_markup()
