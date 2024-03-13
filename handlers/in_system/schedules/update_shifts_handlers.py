from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMSetShifts
from db.requests.with_add import add_shifts
from filters.filters import IsStShiftInStShifts
from handlers.in_system.schedules.functions import update_shifts
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthScheduleCallbackData)

update_shifts_router = Router()


@update_shifts_router.callback_query(
    StateFilter(FSMSetShifts),
    MonthScheduleCallbackData.filter(F.day > 0),
    IsStShiftInStShifts(),
)
async def process_days_press(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
        i18n: dict[str, dict[str, str]],
        state: FSMContext,
        st_shifts: list[dict[str, str]],
):
    markup, st_shifts = await update_shifts(
        session=session,
        i18n=i18n,
        callback=callback,
        callback_data=callback_data,
        default_tz=default_tz,
        st_shifts=st_shifts,
    )
    text: str = i18n['lexicon']['select_days']
    await callback.message.edit_text(
        text=text,
        reply_markup=markup,
    )
    await state.update_data(shifts=st_shifts)


@update_shifts_router.callback_query(
    StateFilter(FSMSetShifts),
    MonthScheduleCallbackData.filter(F.day > 0),
)
async def process_busy_days_press(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
        i18n: dict[str, dict[str, str]],
        state: FSMContext,
):
    markup, st_shifts = await update_shifts(
        session=session,
        i18n=i18n,
        callback=callback,
        callback_data=callback_data,
        default_tz=default_tz,
        state=state,
    )
    text: str = i18n['lexicon']['select_days']
    await callback.message.edit_text(
        text=text,
        reply_markup=markup,
    )
    await state.update_data(shifts=st_shifts)


@update_shifts_router.callback_query(
    StateFilter(FSMSetShifts),
    MonthScheduleCallbackData.filter(F.apply == 1),
)
async def process_apply_in_st(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
        i18n: dict[str, dict[str, str]],
        state: FSMContext,
):
    st: dict[str, list[dict[str, str]]] = await state.get_data()
    st_shifts: list[dict[str, str]] = st["shifts"]
    markup, st_shifts_f = await update_shifts(
        session=session,
        i18n=i18n,
        callback=callback,
        callback_data=callback_data,
        default_tz=default_tz,
        st_shifts=st_shifts,
    )
    if st_shifts_f == st_shifts:
        await add_shifts(
            session=session,
            st_shifts=st_shifts,
        )
        await state.clear()
        markup = await create_month_schedule_v2(
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
        )
        text: str = i18n['lexicon']['shifts_is_apply']
        await callback.message.edit_text(
            text=text,
            reply_markup=markup,
        )
    else:
        text: str = i18n['lexicon']['shifts_is_not_apply']
        await callback.message.edit_text(
            text=text,
            reply_markup=markup,
        )


@update_shifts_router.callback_query(
    StateFilter(FSMSetShifts),
    MonthScheduleCallbackData.filter(F.apply == 2),
)
async def process_cancel_press(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
        i18n: dict[str, dict[str, str]],
        state: FSMContext,
):
    await state.clear()
    markup = await create_month_schedule_v2(
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
    )
    text: str = i18n['lexicon']['select_days']
    await callback.message.edit_text(
        text=text,
        reply_markup=markup,
    )


@update_shifts_router.callback_query(
    StateFilter(FSMSetShifts),
    MonthScheduleCallbackData.filter(),
)
async def process_not_day_press_in_st(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
        i18n: dict[str, dict[str, str]],
        state: FSMContext,
):
    markup, st_shifts = await update_shifts(
        session=session,
        i18n=i18n,
        callback=callback,
        callback_data=callback_data,
        default_tz=default_tz,
        state=state,
    )
    text: str = i18n['lexicon']['select_days']
    await callback.message.edit_text(
        text=text,
        reply_markup=markup,
    )
    await state.update_data(shifts=st_shifts)
