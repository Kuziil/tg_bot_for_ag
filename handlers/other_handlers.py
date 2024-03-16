from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from fluentogram import TranslatorRunner

other_router = Router()


@other_router.message(StateFilter(default_state))
async def send_echo(message: Message, i18n: TranslatorRunner):
    await message.answer(text=i18n.text.other.no())
