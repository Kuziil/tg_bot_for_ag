import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.user import User

from handlers import main_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from config_data.config_reader import settings
from middlewares import DbSessionMiddleware, TranslatorMiddleware
from db.requests import test_connection, check_for_bot_id_in_db
from db.db_helper import DatabaseHelper
from lexicon.lexicon_ru import (
    LEXICON_RU,
    LEXICON_COMMANDS_RU,
    LEXICON_COMMANDS_DESC_RU,
    LEXICON_BUTTON_RU,
    LEXICON_MODELS_RU,
    LEXICON_SHIFTS_RU,
    LEXICON_SCHEDULE_RU,
)
from lexicon.lexicon_en import (
    LEXICON_EN,
    LEXICON_COMMANDS_EN,
    LEXICON_COMMANDS_DESC_EN,
)


# Инициализируем логгер
logger = logging.getLogger(__name__)

translations = {
    "defult": "ru",
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
        "models": LEXICON_MODELS_RU,
        "shifts": LEXICON_SHIFTS_RU,
        "schedule": LEXICON_SCHEDULE_RU,
    },
}


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
    # echo сыпет в консоль
    # pool_size количество подключений
    # max_overflow дополнительные подключения
    db_helper = DatabaseHelper(
        db_url=settings.db_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )

    async with db_helper.sessionmaker() as session:
        await test_connection(session)

    # Инициализируем бот и диспетчер
    dp = Dispatcher(storage=storage)
    dp.update.middleware(
        DbSessionMiddleware(
            session_pool=db_helper.sessionmaker,
        ),
    )
    dp.update.middleware(TranslatorMiddleware())
    # Регистриуем роутеры в диспетчере
    dp.include_router(main_handlers.main_router)
    dp.include_router(other_handlers.router)

    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        parse_mode="HTML",
    )
    info: User = await bot.get_me()
    logger.info(info.id)
    async with db_helper.sessionmaker() as session:
        agenсy: tuple[int, str] = await check_for_bot_id_in_db(
            session=session, bot_id=info.id
        )
    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        agency_id=agenсy[0],
        agency_title=agenсy[1],
        _translations=translations,
    )


if __name__ == "__main__":
    asyncio.run(main())
