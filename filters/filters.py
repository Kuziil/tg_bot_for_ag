from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from emoji import emoji_count
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from db.requests.with_user import is_user_in_agency
from db.requests.with_emoji import is_busy_emoji_in_agency
from keyboards.schedule.month_v2.classes_callback_data import MonthShudleCallbackData


class IsEmoji(BaseFilter):
    async def __call__(
        self,
        message: Message,
    ) -> bool:
        text: str = message.text
        return emoji_count(text) == 1 == len(text)


class IsBusyEmoji(BaseFilter):
    async def __call__(
        self,
        message: Message,
        session: AsyncSession,
        agency_id: int,
    ) -> bool:
        emoji: str = message.text
        return await is_busy_emoji_in_agency(
            session=session,
            agency_id=agency_id,
            emoji=emoji,
        )


class IsUserInSystem(BaseFilter):
    async def __call__(
        self,
        message: Message,
        session: AsyncSession,
        agency_id: int,
    ) -> bool:
        user_tg_id: int = message.from_user.id
        return await is_user_in_agency(
            session=session,
            user_tg_id=user_tg_id,
            agency_id=agency_id,
        )


class IsStShiftInStShifts(BaseFilter):
    async def __call__(
        self,
        callback: CallbackQuery,  # нельзя удалять т.к. callback_data связана
        callback_data: MonthShudleCallbackData,
        state: FSMContext,
    ) -> bool:
        st: dict[str, str] = await state.get_data()
        st_shifts: list[dict[str, str]] = st["shifts"]
        st_shift: dict[str, str] = {
            "day": callback_data.day,
            "month": callback_data.month,
            "year": callback_data.year,
            "page_id": callback_data.page_id,
            "interval_id": callback_data.interval_id,
            "lineup": callback_data.lineup,
            "page_interval_id": callback_data.page_interval_id,
        }
        if st_shift in st_shifts:
            return False
        else:
            st_shifts.append(st_shift)
            return {"st_shifts": st_shifts}
