from aiogram.filters.callback_data import CallbackData


class IntervalCallbackData(
    CallbackData,
    prefix="interval",
    sep="-",
):
    start_at: str
    end_at: str


class PageCallbackData(
    CallbackData,
    prefix="page",
    sep="-",
):
    model_id: int
    page_id: int
    lineup: int
