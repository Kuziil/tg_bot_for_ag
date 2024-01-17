from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import locale
from datetime import datetime
import calendar

from lexicon.lexicon_ru import (
    LEXICON_SCHEDULE_RU,
    LEXICON_MODELS_RU,
    LEXICON_SHIFTS_RU,
    LEXICON_BUTTON_RU
)

locale.setlocale(locale.LC_TIME, 'ru_RU')


class DayCallbackData(CallbackData, prefix='day', sep='-'):
    day: int
    month: int
    year: int


class MonthCallbackData(CallbackData, prefix='month', sep='-'):
    model: str
    number: int
    month: int
    year: int
    napr: int  # 0 - средняя кнопка 1 - назад 2 - вперед


class YearCallbackData(CallbackData, prefix='year', sep='-'):
    model: str
    number: int
    month: int
    year: int
    napr: int  # 0 - средняя кнопка 1 - назад 2 - вперед


class ModelCallbackData(CallbackData, prefix='model', sep='-'):
    model: str
    number: int
    month: int
    year: int
    napr: int  # 0 - средняя кнопка 1 - назад 2 - вперед


class ShiftCallbackData(CallbackData, prefix='shift', sep='-'):
    shift: int
    model: str
    number: int
    month: int
    year: int


def create_schedule(
    month: int = datetime.now().month,
    year: int = datetime.now().year,
    # TODO : Добавить модель дефолт от юзера
    number: int = 0,
    shift: int = 0
) -> InlineKeyboardMarkup:

    match month:
        case 0:
            year -= 1
            month = 12
        case 13:
            year += 1
            month = 1

    models: list[str] = list(LEXICON_MODELS_RU.keys())
    if number == -1:
        number = len(models) - 1
    elif number == len(models) + 1:
        number = 0

    shifts: list[str] = list(LEXICON_SHIFTS_RU.keys())
    if shift == len(shifts):
        shift = 0

    model: str = models[number]

    cal = calendar.monthcalendar(year, month)

    kb_builder = InlineKeyboardBuilder()
    # год
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_year'],
            callback_data=YearCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=1
            ).pack()
        ),
        InlineKeyboardButton(
            text=str(year),
            callback_data=YearCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=0
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_year'],
            callback_data=YearCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=2
            ).pack()
        )
    )
    # месяц
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_month'],
            callback_data=MonthCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=1
            ).pack()
        ),
        InlineKeyboardButton(
            text=str(datetime(year=year, month=month, day=1).strftime('%B')),
            callback_data=MonthCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=0
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_month'],
            callback_data=MonthCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=2
            ).pack()
        )
    )

    # дни недели
    kb_builder.row(
        *[InlineKeyboardButton(
            text=weekday,
            callback_data=f'weekday-{weekday}')
          for weekday in list(calendar.day_abbr)
          ]
    )
    # дни
    for week in cal:
        week_arg = list()
        for day in week:
            day_t = str(day)
            if day == 0:
                day_t = " "
            week_arg.append(InlineKeyboardButton(
                text=day_t,
                callback_data=DayCallbackData(
                    day=day,
                    month=month,
                    year=year
                ).pack()
            ))
        kb_builder.row(
            *week_arg
        )

    # модель
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_model'],
            callback_data=ModelCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=1
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_MODELS_RU[model],
            callback_data=ModelCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=0
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_model'],
            callback_data=ModelCallbackData(
                model=model,
                number=number,
                month=month,
                year=year,
                napr=2
            ).pack()
        )
    )
    # последняя строка
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTON_RU['back'],
            callback_data='back'
        ),
        InlineKeyboardButton(
            text=LEXICON_SHIFTS_RU[shifts[shift]],
            callback_data=ShiftCallbackData(
                shift=shift,
                model=model,
                number=number,
                month=month,
                year=year
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['today'],
            callback_data='today'
        )
    )

    return kb_builder.as_markup()
