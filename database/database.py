from bot import logger
from config_data.config import Config, load_config


class DBManager:
    def __init__(self):
        # Загружаем конфиг в переменную config
        self.config: Config = load_config()

        # Создаем пустой словарь для базы данных
        self.user_database: dict[int, dict] = {}

        self.shifts: dict[str, int] = {}

    # Функция для добавления пользователя
    def add_user(self, user_id: int, username: str, emoticon: str) -> None:
        if user_id not in self.user_database:
            self.user_database[user_id] = {'username': username,
                                           'emoticon': emoticon,
                                           'shifts': []}
            logger.info(f"Пользователь {username} добавлен с ID {user_id}")
        else:
            logger.info(f"Пользователь с ID {user_id} уже существует")

    # Функция для добавления смены пользователю
    # TODO: добавить ответ если пользователь не найден day_t
    def add_shift(self, user_id: int, shift: str) -> str | None:
        if user_id in self.user_database:
            if shift not in self.shifts:
                user = self.user_database[user_id]
                self.shifts[shift] = user_id
                user['shifts'].append(shift)
                logger.info(
                    f"Смена {shift} добавлена пользователю с ID {user_id}")
                return user['emoticon']
            else:
                user_id = self.shifts[shift]
                logger.info(f"Пользователь с ID {user_id} уже занял смену")
                return self.user_database[user_id]['emoticon']
        else:
            logger.info(f"Пользователь с ID {user_id} не найден")
            return '1'

    def get_emot_by_shift(self, shift) -> str:
        return self.user_database[self.shifts[shift]]['emoticon']


# Создаем экземпляр класса
db = DBManager()

# Пример использования методов класса
db.add_user(
    user_id=db.config.tg_bot.admin_ids[0],
    username="Mic",
    emoticon="😏")

db.add_user(
    user_id=db.config.tg_bot.operator_ids[0],
    username="Dac",
    emoticon="🤔")
