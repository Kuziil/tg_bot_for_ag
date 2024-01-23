import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext


from lexicon.lexicon_ru import LEXICON_COMMANDS_RU, LEXICON_RU
from keyboards.kb_single_line_horizontally import create_start_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard
from handlers.in_system.in_systeam_handlers import in_systeam_router
from handlers.not_in_system.not_in_system_handlers import not_in_systeam_router
from FSMs.FSMs import FSMFillForm
from filters.filters import IsUserInSystem


logger = logging.getLogger(__name__)

main_router = Router()

main_router.include_router(not_in_systeam_router)
main_router.include_router(in_systeam_router)


@main_router.message(Command(commands='start'),
                     StateFilter(default_state),
                     IsUserInSystem())
async def process_start_command(message: Message):
    """Данный хэндлер реагирует на команду /start
    выдает список кнопок ориентации в главном меню для Junior

    Args:
        callback (CallbackQuery): _description_
    """
    await message.answer(
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


@main_router.message(Command(commands='start'),
                     StateFilter(default_state))
async def process_start_command_for_new_id(message: Message):
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


@main_router.message(Command(commands='help'),
                     StateFilter(default_state))
async def process_help_command(message: Message):
    """Данный хэндлер служит для предоставления списка команд и
    справки по работе с ботом
    реагирует на /help

    Args:
        message (Message): _description_
    """
    await message.answer(LEXICON_COMMANDS_RU[message.text])


@main_router.callback_query(F.data == 'in_the_system',
                            StateFilter(default_state))
async def process_in_the_system_press(callback: CallbackQuery):
    """Данный хэндлер реагирует на нажатие кнопки в системе
    выдает список кнопок ориентации в главном меню для Junior

    Args:
        callback (CallbackQuery): _description_
    """
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
    await callback.answer()


@main_router.callback_query(F.data == 'not_in_the_system',
                            StateFilter(default_state))
async def process_not_in_the_system_press(callback: CallbackQuery,
                                          state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RU['enter_username']
    )
    await state.set_state(FSMFillForm.fill_username)
