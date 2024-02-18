import logging
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMFillForm
from filters.filters import IsEmoji, IsBusyEmoji
from database.database import db
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.kb_single_line_vertically import create_menu_keyboard
from db.requests import add_user, get_all_emojis_in_agency

logger = logging.getLogger(__name__)
not_in_systeam_router = Router()


@not_in_systeam_router.message(StateFilter(FSMFillForm.fill_username), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(username=message.text)
    await message.answer(
        text=LEXICON_RU["enter_emoticon"],
        reply_markup=create_menu_keyboard("busy_emojis"),
    )
    await state.set_state(FSMFillForm.fill_emoticon)


@not_in_systeam_router.message(StateFilter(FSMFillForm.fill_username))
async def warning_not_name(message: Message):
    await message.answer(
        text=LEXICON_RU["entered_not_username"] + LEXICON_RU["enter_username"]
    )


@not_in_systeam_router.callback_query(
    StateFilter(FSMFillForm.fill_emoticon),
    F.data == "busy_emojis",
)
async def process_show_busy_emojis(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    agency_id: int,
):
    emojis = await get_all_emojis_in_agency(session=session, agency_id=agency_id)
    emojis = "".join(emojis)
    await callback.message.answer(text=emojis)
    await callback.answer()
    await state.set_state(FSMFillForm.fill_emoticon)


@not_in_systeam_router.message(
    StateFilter(FSMFillForm.fill_emoticon), IsEmoji(), IsBusyEmoji()
)
async def warning_busy_emoji(message: Message):
    emojis = ""
    for emoji in db.get_emojis():
        emojis += f"{emoji}"
    await message.answer(text=LEXICON_RU["busy_emoji"] + emojis)


@not_in_systeam_router.message(StateFilter(FSMFillForm.fill_emoticon), IsEmoji())
async def process_emoticon_sent(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    agency_id,
):
    await state.update_data(emoticon=message.text)
    logger.info(await state.get_data())
    st: dict[str, str] = await state.get_data()
    db.user_database[message.from_user.id] = st
    await add_user(
        session=session,
        username=st["username"],
        emoji=st["emoticon"],
        user_tg_id=message.from_user.id,
        agency_id=agency_id,
    )
    await state.clear()
    await message.answer(
        text=LEXICON_RU["registration_done"]
        + f"Приветсвую {db.user_database[message.from_user.id]['username']}"
        f"{db.user_database[message.from_user.id]['emoticon']}\n\n"
        + LEXICON_RU["main_menu_junior"],
        reply_markup=create_menu_keyboard(
            "check_in",
            "clock_out",
            "write_a_report",
            "schedule",
            "my_money",
            "model_statistics",
            "training_materials",
        ),
    )


@not_in_systeam_router.message(StateFilter(FSMFillForm.fill_emoticon))
async def warning_not_emoticon(message: Message):
    await message.answer(text=LEXICON_RU["entered_not_emoticon"])
