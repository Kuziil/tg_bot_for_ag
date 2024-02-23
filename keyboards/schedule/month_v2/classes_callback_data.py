from aiogram.filters.callback_data import CallbackData


class IntervalCallbackData(
    CallbackData,
    prefix="interval",
    sep="-",
):
    start_at: str
    end_at: str
