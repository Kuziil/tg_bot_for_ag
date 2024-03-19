from typing import Sequence

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from callback_factories.back import PagesCallbackData
from db.models import PagesORM
from lexicon.lexicon_ru import LEXICON_BUTTON_RU


# TODO: Отказаться от данного метода
def create_menu_keyboard(
        *buttons: str,
) -> InlineKeyboardMarkup:
    """_summary_
    Данная функция служит конструктором для вертикальной клавиатуры
    на вход получающая теги кнопок
    Returns:
        InlineKeyboardMarkup: _description_
    """
    kb_builder = InlineKeyboardBuilder()
    for button in buttons:
        if button in LEXICON_BUTTON_RU:
            ikb = InlineKeyboardButton(
                text=(
                    LEXICON_BUTTON_RU[button]
                ),
                callback_data=button,
            )
            kb_builder.row(ikb)
        else:
            ikb = InlineKeyboardButton(
                text=(
                    button
                ),
                callback_data=button,
            )
            kb_builder.row(ikb)
    return kb_builder.as_markup()


def create_kb_pages_and_back_forward(
        i18n: TranslatorRunner,
        pages: Sequence[PagesORM],
        user_tg_id: int
):
    kb_builder = InlineKeyboardBuilder()
    for page in pages:
        kb_builder.row(InlineKeyboardButton(text=i18n.button.statistic.page(pageTitle=page.title),
                                            callback_data=PagesCallbackData(page_id=page.id,
                                                                            user_tg_id=user_tg_id).pack()))

    return kb_builder.as_markup()
