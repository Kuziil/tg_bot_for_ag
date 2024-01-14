from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_BUTTON_RU


def create_menu_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    for button in buttons:
        kb_builder.row(InlineKeyboardButton(
            text=LEXICON_BUTTON_RU[button] if button in LEXICON_BUTTON_RU else button,
            callback_data=button
        ))
    return kb_builder.as_markup()
