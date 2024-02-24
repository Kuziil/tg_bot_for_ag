from aiogram.filters.callback_data import CallbackData


class IntervalCallbackData(
    CallbackData,
    prefix="interval",
    sep="-",
):
    start_at: str
    end_at: str
    page_id: int
    lineup: int


class PageCallbackData(
    CallbackData,
    prefix="page",
    sep="-",
):
    page_id: int
    lineup: int
