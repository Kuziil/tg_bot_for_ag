from aiogram.filters.callback_data import CallbackData


class BackCallbackData(
    CallbackData,
    prefix="back",
    sep="-",
):
    handler: str


class ConfirmCallbackData(
    CallbackData,
    prefix='conf',
    sep='-'
):
    day: int
    month: int
    year: int
    page_interval_id: int
    dirty: int
