import logging
from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMFillForm
from db.requests.with_add import add_user
from db.requests.with_emoji import get_str_emojis_in_agency
from filters.filters import IsEmoji, IsBusyEmoji
from keyboards.kb_single_line_vertically import create_menu_keyboard

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)
not_in_agency_router = Router()


@not_in_agency_router.message(
    StateFilter(FSMFillForm.fill_username),
    F.text.isalpha(),
)
async def process_name_sent(
        message: Message,
        state: FSMContext,
        i18n: TranslatorRunner,
):
    await state.update_data(username=message.text)
    await message.answer(
        text=i18n.text.not_in_agency.name.sent(),
        reply_markup=create_menu_keyboard("busy_emojis"),
    )
    await state.set_state(FSMFillForm.fill_emoji)


@not_in_agency_router.message(
    StateFilter(FSMFillForm.fill_username),
)
async def warning_not_name(
        message: Message,
        i18n: TranslatorRunner,
):
    await message.answer(
        text=i18n.text.not_in_agency.name.sent.wrong()
    )


@not_in_agency_router.callback_query(
    StateFilter(FSMFillForm.fill_emoji),
    F.data == "busy_emojis",
)
async def process_show_busy_emojis(
        callback: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
        agency_id: int,
):
    await callback.message.answer(
        text=await get_str_emojis_in_agency(
            session=session,
            agency_id=agency_id,
        ))
    await callback.answer()
    await state.set_state(FSMFillForm.fill_emoji)


@not_in_agency_router.message(
    StateFilter(FSMFillForm.fill_emoji),
    IsEmoji(),
    IsBusyEmoji(),
)
async def warning_busy_emoji(
        message: Message,
        session: AsyncSession,
        agency_id: int,
        i18n: TranslatorRunner,
):
    await message.answer(
        text=i18n.text.not_in_agency.emoji.sent.busy())
    await message.answer(
        text=await get_str_emojis_in_agency(
            session=session,
            agency_id=agency_id,
        ))


@not_in_agency_router.message(
    StateFilter(FSMFillForm.fill_emoji),
    IsEmoji(),
)
async def process_emoji_sent(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        agency_id: int,
        i18n: TranslatorRunner,
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
    await message.answer(
        text=i18n.text.not_in_agency.emoji.sent(),
    )
    await state.clear()


@not_in_agency_router.message(
    StateFilter(FSMFillForm.fill_emoji),
)
async def warning_not_emoji(
        message: Message,
        i18n: TranslatorRunner,
):
    await message.answer(
        text=i18n.text.not_in_agency.emoji.sent.wrong()
    )
    await message.answer(
        text=i18n.text.not_in_agency.emoji.example()
    )
