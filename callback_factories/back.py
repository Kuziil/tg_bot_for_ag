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


class PagesCallbackData(
    CallbackData,
    prefix='pag',
    sep='-'
):
    user_tg_id: int
    page_id: int
