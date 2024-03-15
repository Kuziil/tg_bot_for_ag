from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

router = Router()


@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(text=_("простите, я вас не понимаю"))
