from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.schedule.kb_schedule import (
    create_schedule)
from handlers.in_system.schedule_handlers import schedule_router


in_systeam_router = Router()

in_systeam_router.include_router(schedule_router)


@in_systeam_router.callback_query(F.data == 'schedule',
                                  StateFilter(default_state))
async def process_cal(callback: CallbackQuery):
    """Данный хэндлер отрабатывает на нажатие кнопки расписание ->
    выдает инлайн клавиатуру с расписанием

    Args:
        callback (CallbackQuery): _description_
    """
    await callback.message.edit_text(
        text=LEXICON_RU['schedule'],
        reply_markup=create_schedule()
    )
    await callback.answer()
