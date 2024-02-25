from aiogram.filters.callback_data import CallbackData


class MonthShudleCallbackData(
    CallbackData,
    prefix="interval",
    sep="-",
):
    day: int
    month: int
    year: int
    page_id: int
    lineup: int
    interval_id: int
