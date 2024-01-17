from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery


from lexicon.lexicon_ru import LEXICON_COMMANDS_RU, LEXICON_RU
from keyboards.kb_single_line_horizontally import create_start_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard
from keyboards.schedule.kb_schedule import (
    create_schedule,
    DayCallbackData,
    MonthCallbackData,
    YearCallbackData,
    ModelCallbackData,
    ShiftCallbackData)

# from aiogram_calendar import SimpleCalendar, get_user_locale

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
    """_summary_
    Данный хэндлер служит для предоставления списка команд и
    справки по работе с ботом
    реагирует на /help

    Args:
        message (Message): _description_
    """
    await message.answer(LEXICON_COMMANDS_RU[message.text])


@router.callback_query(F.data == 'in_the_system')
async def process_in_the_system_press(callback: CallbackQuery):
    """_summary_
    Данный хэндлер реагирует на нажатие кнопки в системе
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


# @router.callback_query(F.data == 'schedule')
# async def nav_cal_handler(callback: CallbackQuery):
#     await callback.message.edit_text(
#         "Please select a date: ",
#         reply_markup=await SimpleCalendar(
    # locale=await get_user_locale(callback.from_user)).start_calendar()
#     )


@router.callback_query(F.data == 'schedule')
async def process_cal(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule()
    )


@router.callback_query(DayCallbackData.filter())
async def process_day_press(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['schedule'])
    await callback.answer()


@router.callback_query(MonthCallbackData.filter())
async def process_month_press(callback: CallbackQuery,
                              callback_data: MonthCallbackData):
    call_cal: list[str] = callback_data.pack().split("-")
    napr: int = int(call_cal[5])
    match napr:
        case 1:
            napr = -1
        case 2:
            napr = 1

    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            month=int(call_cal[3])+napr,
            year=int(call_cal[4]),
            number=int(call_cal[2])))
    await callback.answer()


@router.callback_query(YearCallbackData.filter())
async def process_year_press(callback: CallbackQuery,
                             callback_data: YearCallbackData):
    call_cal: list[str] = callback_data.pack().split("-")
    napr: int = int(call_cal[5])
    match napr:
        case 1:
            napr = -1
        case 2:
            napr = 1

    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            month=1,
            year=int(call_cal[4]) + napr,
            number=int(call_cal[2])))
    await callback.answer()


@router.callback_query(ModelCallbackData.filter())
async def process_model_press(callback: CallbackQuery,
                              callback_data: ModelCallbackData):
    call_cal: list[str] = callback_data.pack().split("-")
    napr: int = int(call_cal[5])
    match napr:
        case 1:
            napr = -1
        case 2:
            napr = 1

    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            month=int(call_cal[3]),
            year=int(call_cal[4]),
            number=int(call_cal[2]) + napr))
    await callback.answer()


@router.callback_query(ShiftCallbackData.filter())
async def process_shift_press(callback: CallbackQuery,
                              callback_data: ShiftCallbackData):
    call_cal: list[str] = callback_data.pack().split("-")
    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule(
            month=int(call_cal[4]),
            year=int(call_cal[5]),
            number=int(call_cal[3]),
            shift=int(call_cal[1]) + 1))
    await callback.answer()
