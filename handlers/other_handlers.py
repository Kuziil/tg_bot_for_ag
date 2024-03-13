from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

router = Router()


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
@router.message(StateFilter(default_state))
async def send_echo(message: Message,
                    i18n: dict[str, dict[str, str]],
                    ):
    text: str = i18n['lexicon']['other']
    await message.answer(text=text)
