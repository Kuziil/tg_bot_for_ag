from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

# from lexicon.lexicon_ru import LEXICON_RU
from db.requests import add_model

router = Router()


@router.message(StateFilter(default_state))
async def send_echo(
    message: Message,
    session: AsyncSession,
    agency_id: int,
):
    await add_model(
        session=session,
        agency_id=agency_id,
        model_title=message.text,
    )
    await message.answer(
        text=f"Модель {message.text} добавлена",
    )


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
# @router.message(StateFilter(default_state))
# async def send_echo(message: Message):
#     await message.answer(LEXICON_RU['other'])
