from aiogram.filters.callback_data import CallbackData


class MonthShudleCallbackData(
    CallbackData,
    prefix="interval",
    sep="-",
):
    start_at: str
    end_at: str
    page_id: int
    lineup: int
