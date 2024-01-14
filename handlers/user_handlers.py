from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon_ru import LEXICON_COMMANDS_RU, LEXICON_RU
from keyboards.kb_single_line_horizontally import create_start_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard

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


@router.callback_query(F.data == 'in_the_system')
async def process_in_the_system_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['main_menu_junior'],
        reply_markup=create_menu_keyboard(
            'check_in',
            'clock_out',
            'write_a_report',
            'schedule',
            'my_money',
            'model_statistics',
            'training_materials'
        )
    )
