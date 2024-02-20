from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_BUTTON_RU


def create_start_keyboard(
    *buttons: str,
) -> InlineKeyboardMarkup:
    """_summary_
    Данная функция служит констрктором для горизонтальной клавиатуры
    на вход получающая теги кнопок
    Returns:
        InlineKeyboardMarkup: _description_
    """
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=(
                    LEXICON_BUTTON_RU[button] if button in LEXICON_BUTTON_RU else button
                ),
                callback_data=button,
            )
            for button in buttons
        ]
    )
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
