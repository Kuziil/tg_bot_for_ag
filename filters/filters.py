import logging

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from emoji import is_emoji

from db.models import RolesORM, PermissionsORM
from db.requests.with_emoji import is_busy_emoji_in_agency
from db.requests.with_user import check_user_in_agency_and_get
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthScheduleCallbackData)

logger = logging.getLogger(__name__)


class IsEmoji(BaseFilter):
    async def __call__(
            self,
            message: Message,
    ) -> bool:
        text: str = message.text
        return is_emoji(text)


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


class IsUserInAgencyAndGetRoleDict(BaseFilter):
    async def __call__(
            self,
            message: Message,
            session: AsyncSession,
            agency_id: int,
    ) -> dict[str, dict[str, int | str | list[int] | list[str]]] | bool:
        user_tg_id: int = message.from_user.id
        user = await check_user_in_agency_and_get(
            session=session,
            user_tg_id=user_tg_id,
            agency_id=agency_id,
        )
        if user is None:
            return False
        else:
            role: RolesORM = user.role
            role_dict = {
                "username": user.username,
                "emoji": user.emoji,
                "role_id": role.id,
                "permissions": [],
                "buttons": []
            }
            for permission in role.permissions:  # type: PermissionsORM
                role_dict["permissions"].append(permission.id)
                match permission.id:
                    case 1:
                        role_dict["buttons"].extend(["check_in",
                                                     "write_a_report",
                                                     "schedule",
                                                     "my_money", ])
                    case 3:
                        role_dict["buttons"].append("statistics_of_all_pages")
                return {"role_dict": role_dict}


class IsStShiftInStShifts(BaseFilter):
    async def __call__(
            self,
            callback: CallbackQuery,  # Нельзя удалять т.к. callback_data связана
            callback_data: MonthScheduleCallbackData,
            state: FSMContext,
    ):
        st: dict[str, list[dict[str, int]]] = await state.get_data()
        st_shifts: list[dict[str, int]] = st["shifts"]
        st_shift: dict[str, int] = {
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


class IsIntOrFloat(BaseFilter):
    async def __call__(
            self,
            message: Message
    ):
        text = message.text
        try:
            dirty = int(text)
            return {"dirty": dirty}
        except ValueError:
            try:
                dirty = float(text)
                return {"dirty": dirty}
            except ValueError:
                return False
