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
from FSMs.FSMs import FSMFillForm
from filters.filters import IsEmoji
from database.database import db

logger = logging.getLogger(__name__)

main_router = Router()

main_router.include_router(in_systeam_router)


@main_router.message(Command(commands='start'),
                     StateFilter(default_state))
async def process_start_command(message: Message):
    """Данный хэндлер отвечает на команду /start
    и возвращает текст с кнопками позволяющие пользователю выбрать
    существует ли у него уже аккаунт
    Args:
        message (Message): _description_
    """
    # TODO: убрать если пользователь в системе
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
    await message.answer()


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

# TODO: Переместить в отедельный пакет


@main_router.message(StateFilter(FSMFillForm.fill_username), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(username=message.text)
    # TODO: Предложить посмотреть занятые стикеры
    await message.answer(text=LEXICON_RU['enter_emoticon'])
    await state.set_state(FSMFillForm.fill_emoticon)


@main_router.message(StateFilter(FSMFillForm.fill_username))
async def warning_not_name(message: Message):
    await message.answer(
        text=LEXICON_RU['entered_not_name'] + LEXICON_RU['enter_username']
    )


@main_router.message(StateFilter(FSMFillForm.fill_emoticon),
                     IsEmoji())
async def process_emoticon_sent(message: Message, state: FSMContext):
    await state.update_data(emoticon=message.text)
    # TODO: объеденить следущие две строчки, что бы тратить меньше ресурсов бд
    db.user_database[message.from_user.id] = await state.get_data()
    await db.add_empty_key(message.from_user.id)
    await state.clear()
    await message.answer(
        # TODO: Добавить приветствие по имени и стикеру
        text=LEXICON_RU['registration_done'] +
        LEXICON_RU['main_menu_junior'],
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


@main_router.message(StateFilter(FSMFillForm.fill_emoticon))
async def warning_not_emoticon(message: Message):
    await message.answer(
        text=LEXICON_RU['entered_not_emoticon']
    )

# TODO: Добавить проверку в бд, не занят ли стикер +
# соответсвующий ответ
