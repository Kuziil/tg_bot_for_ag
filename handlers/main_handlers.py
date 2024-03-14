from aiogram import Router, F
from aiogram.filters import Command, StateFilter, or_f, and_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from FSMs.FSMs import FSMFillForm, FSMFillReport
from filters.filters import IsUserInSystem
from handlers.DRY import send_menu_and_clear_state
from handlers.in_system.in_system_handlers import in_system_router
from handlers.not_in_system.not_in_system_handlers import not_in_system_router
from keyboards.kb_single_line_horizontally import create_start_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard

main_router = Router()

main_router.include_router(not_in_system_router)
main_router.include_router(in_system_router)


@main_router.message(
    Command(commands="start"), StateFilter(default_state), IsUserInSystem()
)
async def process_start_command(
        message: Message,
        i18n: dict[str, dict[str, str]],
):
    text: str = i18n["lexicon"]["main_menu_junior"]
    await message.answer(
        text=text,
        reply_markup=create_menu_keyboard(
            "check_in",
            "write_a_report",
            "schedule",
            "my_money",
        ),
    )


@main_router.message(
    Command(commands="start"),
    StateFilter(default_state),
)
async def process_start_command_for_new_id(
        message: Message,
        i18n: dict[str, dict[str, str]],
):
    """Данный хэндлер отвечает на команду /start
    и возвращает текст с кнопками позволяющие пользователю выбрать
    существует ли у него уже аккаунт
    Args:
        i18n:
        message (Message): _description_
    """
    text: str = i18n["commands"][message.text]
    await message.answer(
        text=text,
        reply_markup=create_start_keyboard(
            "not_in_the_system", "in_the_system"),
    )


@main_router.message(
    Command(commands="help"),
    StateFilter(default_state),
)
async def process_help_command(
        message: Message,
        i18n: dict[str, dict[str, str]],
):
    """Данный хэндлер служит для предоставления списка команд и
    справки по работе с ботом
    реагирует на /help

    Args:
        i18n:
        message (Message): _description_
    """
    text: str = i18n["commands"][message.text]
    await message.answer(text=text)


@main_router.callback_query(
    or_f(
        and_f(F.data == "in_the_system", StateFilter(default_state)),
        and_f(F.data == 'back_from_process_send_text', StateFilter(FSMFillReport.dirty))
    ),
)
async def process_in_the_system_press(
        callback: CallbackQuery,
        state: FSMContext,
        i18n: dict[str, dict[str, str]]
):
    text: str = i18n['lexicon']['main_menu_junior']
    await send_menu_and_clear_state(callback=callback, text=text, state=state)


@main_router.callback_query(
    F.data == "not_in_the_system",
    StateFilter(default_state),
)
async def process_not_in_the_system_press(
        callback: CallbackQuery,
        state: FSMContext,
        i18n: dict[str, dict[str, str]]
):
    text: str = i18n["lexicon"]["enter_username"]
    await callback.message.edit_text(text=text)
    await state.set_state(FSMFillForm.fill_username)
