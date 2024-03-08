from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    id: int  # id бота
    admin_ids: list[int]  # Список id администраторов бота
    operator_ids: list[int]  # Список id операторов бота


@dataclass
class DB:
    host: str
    password: str
    name: str
    db_name: str
    port: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DB


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            id=env('BOT_ID'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            operator_ids=list(map(int, env.list('OPERATOR_IDS')))
        ),
        db=DB(
            host=env('DB_HOST'),
            name=env('DB_USER'),
            password=env('DB_PASS'),
            db_name=env('DB_NAME'),
            port=env('DB_PORT')
        )
    )
