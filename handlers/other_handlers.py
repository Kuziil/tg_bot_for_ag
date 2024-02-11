from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon_ru import LEXICON_RU
from db.requests import get_agency_bot_id

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(StateFilter(default_state))
async def send_echo(message: Message, session: AsyncSession):
    # Получаем айди бота с помощью функции get_agency_bot_id
    agency_bot_id = await get_agency_bot_id(session, 1)

    # Отправляем сообщение с айди бота пользователю
    await message.answer(f"Айди бота: {agency_bot_id}")
