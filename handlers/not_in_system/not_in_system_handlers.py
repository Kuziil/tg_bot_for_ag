import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMFillForm
from db.requests.with_add import add_user
from db.requests.with_emoji import get_str_emojis_in_agency
from filters.filters import IsEmoji, IsBusyEmoji
from keyboards.kb_single_line_vertically import create_menu_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.text_processor.processor import text_for_process_emoji_sent

logger = logging.getLogger(__name__)
not_in_system_router = Router()


@not_in_system_router.message(
    StateFilter(FSMFillForm.fill_username),
    F.text.isalpha(),
)
async def process_name_sent(
        message: Message,
        state: FSMContext,
        i18n: dict[str, dict[str, str]]
):
    text: str = i18n["lexicon"]["enter_emoji"]
    await state.update_data(username=message.text)
    await message.answer(
        text=text,
        reply_markup=create_menu_keyboard("busy_emojis"),
    )
    await state.set_state(FSMFillForm.fill_emoji)


@not_in_system_router.message(
    StateFilter(FSMFillForm.fill_username),
)
async def warning_not_name(
        message: Message,
        i18n: dict[str, dict[str, str]]
):
    text: str = i18n["lexicon"]["entered_not_username"]
    await message.answer(
        text=text
    )


@not_in_system_router.callback_query(
    StateFilter(FSMFillForm.fill_emoji),
    F.data == "busy_emojis",
)
async def process_show_busy_emojis(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
        agency_id: int,
):
    text: str = await get_str_emojis_in_agency(
        session=session,
        agency_id=agency_id,
    )
    await callback.message.answer(text=text)
    await callback.answer()
    await state.set_state(FSMFillForm.fill_emoji)


@not_in_system_router.message(
    StateFilter(FSMFillForm.fill_emoji),
    IsEmoji(),
    IsBusyEmoji(),
)
async def warning_busy_emoji(
        message: Message,
        session: AsyncSession,
        i18n: dict[str, dict[str, str]],
        agency_id: int
):
    text_1: str = i18n['lexicon']["busy_emoji"]
    text_2: str = await get_str_emojis_in_agency(
        session=session,
        agency_id=agency_id,
    )
    await message.answer(text=text_1)
    await message.answer(text=text_2)


@not_in_system_router.message(
    StateFilter(FSMFillForm.fill_emoji),
    IsEmoji(),
)
async def process_emoji_sent(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        i18n: dict[str, dict[str, str]],
        agency_id: int,
):
    st: dict[str, str] = await state.get_data()
    emoji: str = message.text
    username: str = st["username"]
    await add_user(
        session=session,
        username=username,
        emoji=emoji,
        user_tg_id=message.from_user.id,
        agency_id=agency_id,
    )
    text: str = await text_for_process_emoji_sent(username=username, emoji=emoji, i18n=i18n)
    await message.answer(
        text=text,
        reply_markup=create_menu_keyboard(
            "check_in",
            "clock_out",
            "write_a_report",
            "schedule",
            "my_money",
        ),
    )
    await state.clear()


@not_in_system_router.message(
    StateFilter(FSMFillForm.fill_emoji),
)
async def warning_not_emoji(
        message: Message,
        i18n: dict[str, dict[str, str]],
):
    text: str = i18n['lexicon']["entered_not_emoji"]
    await message.answer(text=text)
