from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_RU

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(LEXICON_RU['other'])
