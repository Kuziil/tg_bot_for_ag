from zoneinfo import ZoneInfo


from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMSetShifts
from filters.filters import IsStShiftInStShifts
from keyboards.schedule.month_v2.bilder import create_month_shudle_v2
from keyboards.schedule.month_v2.classes_callback_data import MonthShudleCallbackData


update_shifts_router = Router()


@update_shifts_router.callback_query(
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
    markup, st_shifts = await create_month_shudle_v2(
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
    )
    await callback.message.edit_text(
        text="3",
        reply_markup=markup,
    )
    await state.update_data(shifts=st_shifts)


@update_shifts_router.callback_query(
    StateFilter(FSMSetShifts),
    MonthShudleCallbackData.filter(),
)
async def process_not_day_press_in_st(
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
