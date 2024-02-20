from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests import get_emoji_by_user_tg_id


async def create_week_shudle(
    user_tg_id: int,
    session: AsyncSession,
) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        # TODO: добавить сеньера
        InlineKeyboardButton(
            text=await get_emoji_by_user_tg_id(
                session=session,
                user_tg_id=user_tg_id,
            ),
            callback_data="emoji_for_left_up",
        ),
    )

    return kb_builder.as_markup()
