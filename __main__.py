import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.user import User

from handlers import main_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from config_data.config_reader import settings
from middlewares import DbSessionMiddleware
from db.requests import test_connection, check_for_bot_id_in_db
from db.db_helper import DatabaseHelper


# Инициализируем логгер
logger = logging.getLogger(__name__)

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
        i = await check_for_bot_id_in_db(session=session, bot_id=info.id)
        logger.info(i)
    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
