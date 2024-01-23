from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from keyboards.schedule.classes_callback_data import (
    DayCallbackData,
    ModelCallbackData,
    MonthCallbackData,
    ShiftCallbackData,
    YearCallbackData
)
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.schedule.kb_schedule import create_schedule
from database.database import db


schedule_router = Router()


@schedule_router.callback_query(DayCallbackData.filter(),
                                StateFilter(default_state))
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


@schedule_router.callback_query(MonthCallbackData.filter(),
                                StateFilter(default_state))
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


@schedule_router.callback_query(YearCallbackData.filter(),
                                StateFilter(default_state))
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


@schedule_router.callback_query(ModelCallbackData.filter(),
                                StateFilter(default_state))
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


@schedule_router.callback_query(ShiftCallbackData.filter(),
                                StateFilter(default_state))
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


@schedule_router.callback_query(F.data == 'today',
                                StateFilter(default_state))
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
