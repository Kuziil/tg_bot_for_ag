import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter, or_f, and_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from fluentogram import TranslatorRunner

from FSMs.FSMs import FSMFillForm, FSMFillReport
from callback_factories.back import BackCallbackData
from filters.filters import IsUserInAgencyAndGetRoleDict
from handlers.DRY import send_menu_and_clear_state
from handlers.in_system.in_system_handlers import in_agency_router
from handlers.not_in_system.not_in_system_handlers import not_in_agency_router
from keyboards.kb_single_line_horizontally import create_start_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard

main_router = Router()

main_router.include_router(not_in_agency_router)
main_router.include_router(in_agency_router)

logger = logging.getLogger(__name__)


@main_router.message(
    Command(commands="start"), StateFilter(default_state), IsUserInAgencyAndGetRoleDict()
)
async def process_start_command(
        message: Message,
        i18n: TranslatorRunner,
        role_dict: dict[str, int | str | list[int] | list[str]],
):
    await message.answer(
        text=i18n.text.main.menu(userEmoji=role_dict["emoji"], userRole=role_dict['role_title'],
                                 userName=role_dict["username"]),
        reply_markup=create_menu_keyboard(
            *role_dict["buttons"]
        ),
    )


@main_router.message(
    Command(commands="start"),
    StateFilter(default_state),
)
async def process_start_command_for_new_id(
        message: Message,
        i18n: TranslatorRunner,
):
    await message.answer(
        text=i18n.text.main.select_in_or_not(),
        reply_markup=create_start_keyboard(
            "not_in_the_system", "in_the_system"),
    )


@main_router.message(
    Command(commands="help"),
    StateFilter(default_state),
)
async def process_help_command(
        message: Message,
        i18n: TranslatorRunner,
):
    await message.answer(text=i18n.text.main.help())


@main_router.callback_query(
    or_f(
        and_f(F.data == "in_the_system", StateFilter(default_state)),
        and_f(F.data == 'back_from_process_send_text', StateFilter(FSMFillReport.dirty)),
        and_f(BackCallbackData.filter(F.handler == "process_schedule_press"))
    ),
)
async def process_in_the_system_press(
        callback: CallbackQuery,
        state: FSMContext,
        i18n: TranslatorRunner,
):
    await send_menu_and_clear_state(
        callback=callback,
        text=i18n.text.main.menu(),
        state=state)


@main_router.callback_query(
    F.data == "not_in_the_system",
    StateFilter(default_state),
)
async def process_not_in_the_system_press(
        callback: CallbackQuery,
        state: FSMContext,
        i18n: TranslatorRunner,
):
    await callback.message.edit_text(text=i18n.text.main.name.fill())
    await state.set_state(FSMFillForm.fill_username)
