from aiogram.filters import BaseFilter
from aiogram.types import Message
from emoji import emoji_count
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import db
from db.requests import is_user_in_agency, is_busy_emoji_in_agency


class IsEmoji(BaseFilter):
    async def __call__(self, message: Message) -> bool:
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
        return is_busy_emoji_in_agency(
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
