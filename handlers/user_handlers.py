from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_COMMANDS_RU

router = Router()


@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(LEXICON_COMMANDS_RU[message.text])

@router.message(Command(commands='help'))
async def process_start_command(message: Message):
    await message.answer(LEXICON_COMMANDS_RU[message.text])