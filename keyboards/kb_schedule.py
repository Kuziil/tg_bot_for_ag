from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_SCHEDULE_RU, LEXICON_MODELS_RU

def create_schedule() -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_model'],
            callback_data='pre_model'
        ),
        InlineKeyboardButton(
            text=LEXICON_MODELS_RU['Kate'],
            callback_data='Kate'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_model'],
            callback_data='next_model'
        )
    )
    return kb_builder.as_markup()