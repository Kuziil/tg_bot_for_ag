from aiogram.filters.callback_data import CallbackData


class MonthShudleCallbackData(
    CallbackData,
    prefix="interval",
    sep="-",
):
    page_id: int
    lineup: int
    interval_id: int
