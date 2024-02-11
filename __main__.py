import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import main_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from config_data.config_reader import parse_settings, Settings

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from middlewares import DbSessionMiddleware
from db.requests import test_connection

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Инициализируем хранилище
    storage = MemoryStorage()
    # Получаем настройки текущего приложения
    settings: Settings = parse_settings()
    # echo сыпет в консоль
    # pool_size количество подключений
    # max_overflow дополнительные подключения
    engine = create_async_engine(url=str(settings.db_url),
                                 echo=True,
                                 pool_size=5,
                                 max_overflow=10)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    async with sessionmaker() as session:
        await test_connection(session)

    # Инициализируем бот и диспетчер
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    # Регистриуем роутеры в диспетчере
    dp.include_router(main_handlers.main_router)
    dp.include_router(other_handlers.router)

    bot = Bot(token=settings.bot_token.get_secret_value(),
              parse_mode='HTML')

    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
