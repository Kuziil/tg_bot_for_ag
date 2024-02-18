import logging

from config_data.config import Config, load_config
from lexicon.lexicon_ru import LEXICON_BUTTON_RU

logger = logging.getLogger(__name__)


class DBManager:
    def __init__(self):
        # Загружаем конфиг в переменную config
        self.config: Config = load_config()

        # Создаем пустой словарь для базы данных
        bot_id = self.config.tg_bot.id
        self.user_databases: dict[int, dict[int, dict[str, str | list[str]]]] = {
            bot_id: dict()
        }

        self.shifts: dict[str, int] = {}

        self.user_database: dict[int, dict[str, str | list[str]]] = self.user_databases[
            bot_id
        ]

    # Функция проверки на наличие пользователя в системе
    # Заменил
    def is_user_in_system(self, user_id: int) -> bool:
        return True if user_id in self.user_database else False

    # Функция для добавления пользователя
    def add_user(self, user_id: int, username: str, emoticon: str) -> None:
        if self.is_user_in_system(user_id=user_id):
            logger.info(f"Пользователь с ID {user_id} уже существует")
        else:
            self.user_database[user_id] = {
                "username": username,
                "emoticon": emoticon,
                "shifts": [],
            }
            logger.info(f"Пользователь {username} добавлен с ID {user_id}")

    # Функция для добавления смены пользователю
    def add_shift(self, user_id: int, day_call_back_t: str) -> str | None:
        if self.is_user_in_system(user_id=user_id):
            if day_call_back_t not in self.shifts:
                user = self.user_database[user_id]
                self.shifts[day_call_back_t] = user_id
                user["shifts"].append(day_call_back_t)
                return user["emoticon"]
            else:
                user_id = self.shifts[day_call_back_t]
                return self.user_database[user_id]["emoticon"]
        else:
            return LEXICON_BUTTON_RU["user_not_in_system"]

    def get_emot_by_day_call_back(self, shift) -> str:
        return self.user_database[self.shifts[shift]]["emoticon"]


# Создаем экземпляр класса
db = DBManager()
