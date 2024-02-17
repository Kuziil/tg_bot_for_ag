from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

# from lexicon.lexicon_ru import LEXICON_RU
from db.requests import get_agency_bot_id, is_user_in_agency

router = Router()


@router.message(StateFilter(default_state))
async def send_echo(
    message: Message,
    session: AsyncSession,
    agency_id: int,
):
    # Получаем айди бота с помощью функции get_agency_bot_id
    user_tg_id = message.from_user.id
    agency_bot_id = await is_user_in_agency(
        session=session,
        user_tg_id=user_tg_id,
        agency_id=agency_id,
    )

    # Отправляем сообщение с айди бота пользователю
    await message.answer(f"Айди бота: {agency_bot_id}")


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
# @router.message(StateFilter(default_state))
# async def send_echo(message: Message):
#     await message.answer(LEXICON_RU['other'])
