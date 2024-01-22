import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from lexicon.lexicon_ru import LEXICON_COMMANDS_RU
from keyboards.kb_single_line_horizontally import create_start_keyboard
from handlers import in_systeam_handlers

logger = logging.getLogger(__name__)

main_router = Router()

main_router.include_router(in_systeam_handlers.in_systeam_router)


@main_router.message(Command(commands='start'))
async def process_start_command(message: Message):
    """Данный хэндлер отвечает на команду /start
    и возвращает текст с кнопками позволяющие пользователю выбрать
    существует ли у него уже аккаунт
    Args:
        message (Message): _description_
    """
    text = LEXICON_COMMANDS_RU[message.text]
    await message.answer(
        text=text,
        reply_markup=create_start_keyboard(
            'not_in_the_system',
            'in_the_system'
        )
    )


@main_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """Данный хэндлер служит для предоставления списка команд и
    справки по работе с ботом
    реагирует на /help

    Args:
        message (Message): _description_
    """
    await message.answer(LEXICON_COMMANDS_RU[message.text])
    await message.answer()
