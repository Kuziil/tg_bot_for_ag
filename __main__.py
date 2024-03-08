import asyncio
import locale
import logging
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.user import User

from config_data.config_reader import settings
from db.db_helper import DatabaseHelper
from db.requests.with_test import check_for_bot_id_in_db
from db.requests.with_test import test_connection
from handlers import main_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from lexicon.lexicon_en import (
    LEXICON_EN,
    LEXICON_COMMANDS_EN,
    LEXICON_COMMANDS_DESC_EN,
)
from lexicon.lexicon_ru import (
    LEXICON_RU,
    LEXICON_COMMANDS_RU,
    LEXICON_COMMANDS_DESC_RU,
    LEXICON_BUTTON_RU,
)
from middlewares import DbSessionMiddleware, TranslatorMiddleware

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Инициализируем локализатор для перевода текста
translations = {
    "default": "ru",
    "en": {
        "lexicon": LEXICON_EN,
        "commands": LEXICON_COMMANDS_EN,
        "commands_desc": LEXICON_COMMANDS_DESC_EN,
    },
    "ru": {
        "lexicon": LEXICON_RU,
        "commands": LEXICON_COMMANDS_RU,
        "commands_desc": LEXICON_COMMANDS_DESC_RU,
        "button": LEXICON_BUTTON_RU,
    },
}

locale.setlocale(locale.LC_TIME, "ru_RU.UTF8")


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # Инициализируем хранилище
    storage = MemoryStorage()

    # Инициализируем хелпер для базы данных
    db_helper = DatabaseHelper(
        db_url=settings.db_url,
        echo=False,  # Режим отладки
        pool_size=5,  # Количество подключений
        max_overflow=10,  # Максимальное количество подключений
    )

    # проверяем соединение с базой данных
    async with db_helper.sessionmaker() as session:
        await test_connection(session)

    # Инициализируем диспетчер
    dp = Dispatcher(storage=storage)

    # Регистрируем мидлвари в диспетчере
    dp.update.middleware(
        DbSessionMiddleware(
            session_pool=db_helper.sessionmaker,
        ),
    )
    dp.update.middleware(
        TranslatorMiddleware(),
    )

    # Регистрируем роутеры в диспетчере
    dp.include_router(main_handlers.main_router)
    dp.include_router(other_handlers.router)

    # Инициализируем бота и получаем информацию о нем от API Telegram.
    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        parse_mode="HTML",
    )

    # Проверяем действительный ли бот
    info: User = await bot.get_me()
    async with db_helper.sessionmaker() as session:
        agency: tuple[int, str] = await check_for_bot_id_in_db(
            session=session, bot_id=info.id
        )

    # устанавливаем меню для бота
    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        agency_id=agency[0],
        agency_title=agency[1],
        _translations=translations,
        # TODO: подтянуть из бд
        default_tz=ZoneInfo("Europe/Moscow"),
    )


if __name__ == "__main__":
    asyncio.run(main())
