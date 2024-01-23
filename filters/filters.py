from aiogram.filters import BaseFilter
from aiogram.types import Message
from emoji import emoji_count

from database.database import db


class IsEmoji(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        text: str = message.text
        return emoji_count(text) == 1 == len(text)


class IsUserInSystem(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id: int = message.from_user.id
        return db.is_user_in_system(user_id=user_id)
