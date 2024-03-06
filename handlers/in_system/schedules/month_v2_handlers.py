from zoneinfo import ZoneInfo
import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.schedule.month_v2.classes_callback_data import (
    MonthScheduleCallbackData,
)
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from FSMs.FSMs import FSMSetShifts
from handlers.in_system.schedules.update_shifts_handlers import (
    update_shifts_router)


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
    i18n: dict[str, dict[str, str]],
    state: FSMContext,
):
    logger.debug("process_first_day_press - start")
    st_shifts: list[dict[str, str | int]] = []
    st_shift: dict[str, str | int] = {
        "day": callback_data.day,
        "month": callback_data.month,
        "year": callback_data.year,
        "page_id": callback_data.page_id,
        "interval_id": callback_data.interval_id,
        "lineup": callback_data.lineup,
        "page_interval_id": callback_data.page_interval_id,
    }
    st_shifts.append(st_shift)
    logger.debug(f"st_shifts: {st_shifts}")
    markup, st_shifts = await create_month_schedule_v2(
        user_tg_id=callback.from_user.id,
        session=session,
        i18n=i18n,
        default_tz=default_tz,
        current_month=callback_data.month,
        current_year=callback_data.year,
        current_day=callback_data.day,
        current_page_id=callback_data.page_id,
        current_interval_id=callback_data.interval_id,
        current_lineup=callback_data.lineup,
        st_shifts=st_shifts,
    )
    await callback.message.edit_text(
        text="3",
        reply_markup=markup,
    )
    await state.set_state(FSMSetShifts.shifts)
    await state.update_data(shifts=st_shifts)
    logger.debug("process_first_day_press - finish")


@month_v2_router.callback_query(
    StateFilter(default_state),
    MonthScheduleCallbackData.filter(),
)
async def process_not_day_press(
    callback: CallbackQuery,
    callback_data: MonthScheduleCallbackData,
    session: AsyncSession,
    default_tz: ZoneInfo,
    i18n: dict[dict[str, str]],
):
    logger.debug("process_not_day_press - start")
    await callback.message.edit_text(
        text="2",
        reply_markup=await create_month_schedule_v2(
            user_tg_id=callback.from_user.id,
            session=session,
            i18n=i18n,
            default_tz=default_tz,
            current_month=callback_data.month,
            current_year=callback_data.year,
            current_day=callback_data.day,
            current_page_id=callback_data.page_id,
            current_interval_id=callback_data.interval_id,
            current_lineup=callback_data.lineup,
        ),
    )
    await callback.answer()
    logger.debug("process_not_day_press - finish")
