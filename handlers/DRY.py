from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.kb_single_line_vertically import create_menu_keyboard


async def send_menu_and_clear_state(callback: CallbackQuery,
                                    text: str,
                                    state: FSMContext, ):
    await state.clear()
    await callback.message.edit_text(
        text=text,
        reply_markup=create_menu_keyboard(
            "check_in",
            "clock_out",
            "write_a_report",
            "schedule",
            "my_money",
        ),
    )
    await callback.answer()
