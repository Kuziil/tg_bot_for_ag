import logging
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import gettext as _

from FSMs.FSMs import FSMSetShifts
from handlers.in_system.schedules.functions import update_shifts
from handlers.in_system.schedules.update_shifts_handlers import (
    update_shifts_router)
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthScheduleCallbackData,
)

month_v2_router = Router()

month_v2_router.include_router(update_shifts_router)

logger = logging.getLogger(__name__)


@month_v2_router.callback_query(
    StateFilter(default_state),
    MonthScheduleCallbackData.filter(F.day > 0),
)
async def process_first_day_press(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
        state: FSMContext,
):
    markup, st_shifts = await update_shifts(session=session, callback=callback, callback_data=callback_data,
                                            default_tz=default_tz, state=state)
    await callback.message.edit_text(
        text=_('Выберите даты на которые выйдете'),
        reply_markup=markup,
    )
    await state.set_state(FSMSetShifts.shifts)
    await state.update_data(shifts=st_shifts)


@month_v2_router.callback_query(
    StateFilter(default_state),
    MonthScheduleCallbackData.filter(),
)
async def process_not_day_press(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
):
    markup = await create_month_schedule_v2(
        user_tg_id=callback.from_user.id,
        session=session,
        default_tz=default_tz,
        current_month=callback_data.month,
        current_year=callback_data.year,
        current_day=callback_data.day,
        current_page_id=callback_data.page_id,
        current_interval_id=callback_data.interval_id,
        current_lineup=callback_data.lineup,
    )
    await callback.message.edit_text(
        text=_('Пожалуйста выберите страницу и дату смены'),
        reply_markup=markup
    )
    await callback.answer()
