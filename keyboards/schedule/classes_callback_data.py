from aiogram.filters.callback_data import CallbackData


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