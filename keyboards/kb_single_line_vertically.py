from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_BUTTON_RU


def create_menu_keyboard(
    *buttons: str,
) -> InlineKeyboardMarkup:
    """_summary_
    Данная функция служит конструктором для вертикальной клавиатуры
    на вход получающая теги кнопок
    Returns:
        InlineKeyboardMarkup: _description_
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    for button in buttons:
        kb_builder.row(
            InlineKeyboardButton(
                text=(
                    LEXICON_BUTTON_RU[button] if button in LEXICON_BUTTON_RU else button
                ),
                callback_data=button,
            )
        )
    return kb_builder.as_markup()
