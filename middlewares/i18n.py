from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        # user_lang = user.language_code
        translations: dict[str, dict[str, str]] = data.get("_translations")
        # вернуть эту строчку если понадобиться локализация
        # i18n = translations.get(user_lang)
        i18n = None
        if i18n is None:
            data["i18n"] = translations[translations["default"]]
        else:
            data["i18n"] = i18n

        return await handler(event, data)
