from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_COMMANDS_RU
from keyboards.kb import create_start_keyboard

router = Router()


@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    """_summary_
    Данный хэндлер отвечает на команду /start
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


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON_COMMANDS_RU[message.text])
