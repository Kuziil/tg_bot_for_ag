from zoneinfo import ZoneInfo

from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.schedule.month_v2.builder import create_month_schedule_v2


async def update_shifts(session: AsyncSession, i18n: dict[str, dict[str, str]], callback, callback_data,
                        default_tz: ZoneInfo,
                        st_shifts: list[dict[str, str]] | None = None,
                        state: FSMContext | None = None, ):
    if st_shifts is None:
        st: dict[str, list[dict[str, str]]] = await state.get_data()
        st_shifts: list[dict[str, str]] = st["shifts"]

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
    return markup, st_shifts
