from aiogram.filters.callback_data import CallbackData


class MonthShudleCallbackData(
    CallbackData,
    prefix="shu",
    sep="-",
):
    day: int
    month: int
    year: int
    page_id: int
    lineup: int
    interval_id: int
    apply: int
