from aiogram.filters import BaseFilter
from aiogram.types import Message
from emoji import emoji_count


class IsEmoji(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        text: str = message.text
        return emoji_count(text) == 1 == len(text)
