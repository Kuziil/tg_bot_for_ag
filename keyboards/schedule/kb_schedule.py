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
    month: int
    year: int
    napr: int  # 0 - средняя кнопка 1 - назад 2 - вперед


class YearCallbackData(CallbackData, prefix='year', sep='-'):
    year: int
    napr: int  # 0 - средняя кнопка 1 - назад 2 - вперед


def create_schedule(
    month: int = datetime.now().month,
    year: int = datetime.now().year
) -> InlineKeyboardMarkup:

    match month:
        case 0:
            year -= 1
            month = 12
        case 13:
            year += 1
            month = 1

    cal = calendar.monthcalendar(year, month)

    kb_builder = InlineKeyboardBuilder()
    # год
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_year'],
            callback_data=YearCallbackData(
                year=year,
                napr=1
            ).pack()
        ),
        InlineKeyboardButton(
            text=str(year),
            callback_data=YearCallbackData(
                year=year,
                napr=0
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_year'],
            callback_data=YearCallbackData(
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
                month=month,
                year=year,
                napr=1
            ).pack()
        ),
        InlineKeyboardButton(
            text=str(month),
            callback_data=MonthCallbackData(
                month=month,
                year=year,
                napr=0
            ).pack()
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_month'],
            callback_data=MonthCallbackData(
                month=month,
                year=year,
                napr=2
            ).pack()
        )
    )

    # дни недели
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['monday'],
            callback_data='monday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['tuesday'],
            callback_data='tuesday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['wednesday'],
            callback_data='wednesday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['thursday'],
            callback_data='thursday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['friday'],
            callback_data='friday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['saturday'],
            callback_data='saturday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['sunday'],
            callback_data='sunday'
        )
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
            callback_data='pre_model'
        ),
        InlineKeyboardButton(
            text=list(LEXICON_MODELS_RU.values())[0],
            callback_data=list(LEXICON_MODELS_RU.keys())[0]
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_model'],
            callback_data='next_model'
        )
    )
    # последняя строка
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTON_RU['back'],
            callback_data='back'
        ),
        InlineKeyboardButton(
            text=list(LEXICON_SHIFTS_RU.values())[0],
            callback_data=list(LEXICON_SHIFTS_RU.keys())[0]
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['today'],
            callback_data='today'
        )
    )

    return kb_builder.as_markup()
