import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.schedule.classes_callback_data import (
    DayCallbackData,
    ModelCallbackData,
    MonthCallbackData,
    ShiftCallbackData,
    YearCallbackData
)
from lexicon.lexicon_ru import LEXICON_COMMANDS_RU, LEXICON_RU
from keyboards.kb_single_line_horizontally import create_start_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard
from keyboards.schedule.kb_schedule import (
    create_schedule)
from database.database import db

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command(commands='start'))
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


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    """Данный хэндлер служит для предоставления списка команд и
    справки по работе с ботом
    реагирует на /help

    Args:
        message (Message): _description_
    """
    await message.answer(LEXICON_COMMANDS_RU[message.text])
    await message.answer()


@router.callback_query(F.data == 'in_the_system')
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


@router.callback_query(F.data == 'schedule')
async def process_cal(callback: CallbackQuery):
    """Данный хэндлер отрабатывает на нажатие кнопки расписание ->
    выдает инлайн клавиатуру с расписанием

    Args:
        callback (CallbackQuery): _description_
    """
    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule()
    )
    await callback.answer()

# TODO: прописать реакцию при нажатии на кнопку


@router.callback_query(DayCallbackData.filter())
async def process_day_press(callback: CallbackQuery,
                            callback_data: DayCallbackData):
    """Данный хэндлер срабатывает при нажатие на любую дату
    Args:
        callback (CallbackQuery): _description_
    """
    user_id = callback.from_user.id
    await callback.message.edit_text(
        text=LEXICON_RU['schedule'] if
        db.is_user_in_system(user_id=user_id)
        else LEXICON_RU['user_not_in_system'],
        reply_markup=create_schedule(
            user_id=user_id,
            day=callback_data.day,
            month=callback_data.month,
            year=callback_data.year,
            number=callback_data.number,
            shift=callback_data.shift))
    await callback.answer()


@router.callback_query(MonthCallbackData.filter())
async def process_month_press(callback: CallbackQuery,
                              callback_data: MonthCallbackData):
    """Этот хэндлер срабатывает при нажатии на кнопки ответственные за месяцы
    если napr 0 то состояние неизменно
    если napr 1 то следущий месяц
    если napr 2 то предыдущий месяц
    Args:
        callback (CallbackQuery): _description_
        callback_data (MonthCallbackData): _description_
    """
    napr: int = callback_data.napr
    match napr:
        case 1:
            napr = -1
        case 2:
            napr = 1

    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            shift=callback_data.shift,
            month=callback_data.month+napr,
            year=callback_data.year,
            number=callback_data.number))
    await callback.answer()


@router.callback_query(YearCallbackData.filter())
async def process_year_press(callback: CallbackQuery,
                             callback_data: YearCallbackData):
    """Этот хэндлер срабатывает при нажатии на кнопки ответственные за год
    если napr 0 то состояние неизменно
    если napr 1 то следущий месяц
    если napr 2 то предыдущий месяц
    Args:
        callback (CallbackQuery): _description_
        callback_data (MonthCallbackData): _description_
    """
    napr: int = callback_data.napr
    match napr:
        case 1:
            napr = -1
        case 2:
            napr = 1

    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            shift=callback_data.shift,
            month=1,
            year=callback_data.year + napr,
            number=callback_data.number))
    await callback.answer()


@router.callback_query(ModelCallbackData.filter())
async def process_model_press(callback: CallbackQuery,
                              callback_data: ModelCallbackData):
    """Этот хэндлер срабатывает при нажатии на кнопки ответственные за модель
    если napr 0 то состояние неизменно
    если napr 1 то следущий месяц
    если napr 2 то предыдущий месяц
    Args:
        callback (CallbackQuery): _description_
        callback_data (MonthCallbackData): _description_
    """
    napr: int = callback_data.napr
    match napr:
        case 1:
            napr = -1
        case 2:
            napr = 1

    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            shift=callback_data.shift,
            month=callback_data.month,
            year=callback_data.year,
            number=callback_data.number + napr))
    await callback.answer()


@router.callback_query(ShiftCallbackData.filter())
async def process_shift_press(callback: CallbackQuery,
                              callback_data: ShiftCallbackData):
    """Этот хэндлер срабатывает при нажатии на кнопку ответственную за смену
    Args:
        callback (CallbackQuery): _description_
        callback_data (MonthCallbackData): _description_
    """
    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            month=callback_data.month,
            year=callback_data.year,
            number=callback_data.number,
            shift=callback_data.shift + 1))
    await callback.answer()


@router.callback_query(F.data == 'today')
async def process_today(callback: CallbackQuery):
    """Данный хэндлер отрабатывает на нажатие кнопки сегодня ->
    переносит расписание на текущую дату.
    Args:
        callback (CallbackQuery): _description_
    """
    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule()
    )
    await callback.answer()
