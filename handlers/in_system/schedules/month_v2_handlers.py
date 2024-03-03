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
from handlers.in_system.schedules.update_shifts_handlers import update_shifts_router


month_v2_router = Router()

month_v2_router.include_router(update_shifts_router)


@month_v2_router.callback_query(
    StateFilter(default_state),
    MonthShudleCallbackData.filter(F.day == 0 | F.day == None),
)
async def process_not_day_press(
    callback: CallbackQuery,
    callback_data: MonthShudleCallbackData,
    session: AsyncSession,
    defult_tz: ZoneInfo,
    i18n: dict[dict[str, str]],
):
    print("process_not_day_press")
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
