from aiogram.filters.callback_data import CallbackData


class BackCallbackData(
    CallbackData,
    prefix="back",
    sep="-",
):
    handler: str
