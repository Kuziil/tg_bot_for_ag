from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_SCHEDULE_RU, LEXICON_MODELS_RU, LEXICON_SHIFTS_RU, LEXICON_BUTTON_RU


def create_schedule() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    # год
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_year'],
            callback_data='pre_year'
        ),
        InlineKeyboardButton(
            text='2024',
            callback_data='2024'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_year'],
            callback_data='next_year'
        )
    )
    # месяц
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_month'],
            callback_data='pre_month'
        ),
        InlineKeyboardButton(
            text='Январь',
            callback_data='Jan'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_month'],
            callback_data='next_month'
        )
    )
    # дни недели
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['monday'],
            callback_data='monday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['tuesday'],
            callback_data='tuesday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['wednesday'],
            callback_data='wednesday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['thursday'],
            callback_data='thursday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['friday'],
            callback_data='friday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['saturday'],
            callback_data='saturday'
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['sunday'],
            callback_data='sunday'
        )
    )
    # дни
    for line in range(1, 7):
        kb_builder.row(
            *[InlineKeyboardButton(text=str(line * column), callback_data=str(line * column)) for column in range(1, 7)]
        )
    # модель
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['pre_model'],
            callback_data='pre_model'
        ),
        InlineKeyboardButton(
            text=list(LEXICON_MODELS_RU.values())[0],
            callback_data=list(LEXICON_MODELS_RU.keys())[0]
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['next_model'],
            callback_data='next_model'
        )
    )
    # последняя строка
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_BUTTON_RU['back'],
            callback_data='back'
        ),
        InlineKeyboardButton(
            text=list(LEXICON_SHIFTS_RU.values())[0],
            callback_data=list(LEXICON_SHIFTS_RU.keys())[0]
        ),
        InlineKeyboardButton(
            text=LEXICON_SCHEDULE_RU['today'],
            callback_data='today'
        )
    )

    return kb_builder.as_markup()
