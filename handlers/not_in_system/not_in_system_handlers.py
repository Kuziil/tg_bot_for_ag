import logging

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMFillForm
from db.requests.with_add import add_user
from db.requests.with_emoji import get_str_emojis_in_agency
from filters.filters import IsEmoji, IsBusyEmoji
from keyboards.kb_single_line_vertically import create_menu_keyboard
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
):
    await state.update_data(username=message.text)
    await message.answer(
        text=_("Имя принято.\n\n"
               "Пожалуйста, отправьте эмодзи из классического набора.\n"
               "Если стикер будет добавлен из Telegram Premium,"
               "то он будет автоматически отформатирован.\n"
               "Эмодзи нужно отправить без дополнительных символов\n"
               "В дальнейшем можно всегда заменить эмодзи"),
        reply_markup=create_menu_keyboard("busy_emojis"),
    )
    await state.set_state(FSMFillForm.fill_emoji)


@not_in_system_router.message(
    StateFilter(FSMFillForm.fill_username),
)
async def warning_not_name(
        message: Message,
):
    await message.answer(
        text=_("Данное имя не подходит, "
               "оно содержит не только буквы\n\n"
               "Пожалуйста введите свое имя\n"
               "Имя должно состоять полностью из букв")
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
    await callback.message.answer(
        text=await get_str_emojis_in_agency(
            session=session,
            agency_id=agency_id,
        ))
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
        agency_id: int
):
    await message.answer(
        text=_("Данное эмодзи уже занято, выберете,"
               "то которое не входит в данный список\n\n"))
    await message.answer(
        text=await get_str_emojis_in_agency(
            session=session,
            agency_id=agency_id,
        ))


@not_in_system_router.message(
    StateFilter(FSMFillForm.fill_emoji),
    IsEmoji(),
)
async def process_emoji_sent(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
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
    await message.answer(
        text=await text_for_process_emoji_sent(username=username, emoji=emoji),
        reply_markup=create_menu_keyboard(
            "check_in",
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
):
    await message.answer(
        text=_("Вы допустили ошибку, при вводе эмодзи\n\n"
               "Пожалуйста, отправьте только эмодзи\n"
               "Например: 🙈")
    )
