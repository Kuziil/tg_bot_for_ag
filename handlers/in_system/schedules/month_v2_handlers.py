from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.schedule.month_v2.classes_callback_data import (
    MonthShudleCallbackData,
)
from keyboards.schedule.month_v2.bilder import create_month_shudle_v2


month_v2_router = Router()


@month_v2_router.callback_query(
    StateFilter(default_state),
    MonthShudleCallbackData.filter(),
)
async def process_day_press(
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
            current_page_id=callback_data.page_id,
            current_interval_id=callback_data.interval_id,
            current_lineup=callback_data.lineup,
        ),
    )
    await callback.answer()
