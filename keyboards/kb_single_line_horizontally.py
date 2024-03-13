from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_factories.back import ConfirmCallbackData
from lexicon.lexicon_ru import LEXICON_BUTTON_RU


def create_start_keyboard(
        *buttons: str,
) -> InlineKeyboardMarkup:
    """_summary_
    Данная функция служит конструктором для горизонтальной клавиатуры
    на вход получающая теги кнопок
    Returns:
        InlineKeyboardMarkup: _description_
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    ikb_buttons = []
    for button in buttons:
        if button in LEXICON_BUTTON_RU:
            ikb = InlineKeyboardButton(
                text=(
                    LEXICON_BUTTON_RU[button]
                ),
                callback_data=button,
            )
        else:
            ikb = InlineKeyboardButton(
                text=(
                    button
                ),
                callback_data=button,
            )
        ikb_buttons.append(ikb)

    # Добавляем в билдер ряд с кнопками
    kb_builder.row(
        *ikb_buttons
    )
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


async def create_confirm_keyboard(
        day: int,
        month: int,
        year: int,
        page_interval_id: int,
        dirty: int,
):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text="not_confirm",
            callback_data="not_confirm"
        ),
        InlineKeyboardButton(
            text="confirm",
            callback_data=ConfirmCallbackData(
                day=day,
                month=month,
                year=year,
                page_interval_id=page_interval_id,
                dirty=dirty
            ).pack()
        )
    )
    return kb_builder.as_markup()
