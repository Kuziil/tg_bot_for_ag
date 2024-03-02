from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.schedule.month_v2.classes_callback_data import (
    MonthShudleCallbackData,
)
from keyboards.schedule.month_v2.bilder import create_month_shudle_v2
from FSMs.FSMs import FSMSetShifts
from filters.filters import IsStShiftInStShifts


month_v2_router = Router()


@month_v2_router.callback_query(
    StateFilter(default_state),
    MonthShudleCallbackData.filter(F.day > 0),
)
async def process_first_day_press(
    callback: CallbackQuery,
    callback_data: MonthShudleCallbackData,
    session: AsyncSession,
    defult_tz: ZoneInfo,
    i18n: dict[dict[str, str]],
    state: FSMContext,
):
    st_shifts: list[dict[str, str]] = []
    st_shift: dict[str, str] = {
        "day": callback_data.day,
        "month": callback_data.month,
        "year": callback_data.year,
        "interval_id": callback_data.interval_id,
    }
    st_shifts.append(st_shift)
    await state.set_state(FSMSetShifts.shifts)
    await state.update_data(shifts=st_shifts)
    # st: dict[str, str] = await state.get_data()
    # await callback.message.answer(text=f'{st["shifts"][0]["day"]}')
    await callback.message.edit_text(
        text="3",
        reply_markup=await create_month_shudle_v2(
            user_tg_id=callback.from_user.id,
            session=session,
            i18n=i18n,
            defult_tz=defult_tz,
            current_month=callback_data.month,
            current_year=callback_data.year,
            current_day=callback_data.day,
            current_page_id=callback_data.page_id,
            current_interval_id=callback_data.interval_id,
            current_lineup=callback_data.lineup,
            st_shifts=st_shifts,
        ),
    )


@month_v2_router.callback_query(
    StateFilter(FSMSetShifts),
    MonthShudleCallbackData.filter(F.day > 0),
    IsStShiftInStShifts(),
)
async def process_days_press(
    callback: CallbackQuery,
    callback_data: MonthShudleCallbackData,
    session: AsyncSession,
    defult_tz: ZoneInfo,
    i18n: dict[dict[str, str]],
    state: FSMContext,
    st_shifts: list[dict[str, str]],
):
    await state.update_data(shifts=st_shifts)
    await callback.message.edit_text(
        text="4",
        reply_markup=await create_month_shudle_v2(
            user_tg_id=callback.from_user.id,
            session=session,
            i18n=i18n,
            defult_tz=defult_tz,
            current_month=callback_data.month,
            current_year=callback_data.year,
            current_day=callback_data.day,
            current_page_id=callback_data.page_id,
            current_interval_id=callback_data.interval_id,
            current_lineup=callback_data.lineup,
            st_shifts=st_shifts,
        ),
    )


@month_v2_router.callback_query(
    StateFilter(default_state),
    MonthShudleCallbackData.filter(),
)
async def process_not_day_press(
    callback: CallbackQuery,
    callback_data: MonthShudleCallbackData,
    session: AsyncSession,
    defult_tz: ZoneInfo,
    i18n: dict[dict[str, str]],
):
    await callback.message.edit_text(
        text="2",
        reply_markup=await create_month_shudle_v2(
            user_tg_id=callback.from_user.id,
            session=session,
            i18n=i18n,
            defult_tz=defult_tz,
            current_month=callback_data.month,
            current_year=callback_data.year,
            current_day=callback_data.day,
            current_page_id=callback_data.page_id,
            current_interval_id=callback_data.interval_id,
            current_lineup=callback_data.lineup,
        ),
    )
    await callback.answer()
