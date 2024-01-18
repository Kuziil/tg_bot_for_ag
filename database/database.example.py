from bot import logger

# Создаем пустой словарь для базы данных
user_database: dict[int, dict] = {}

# {1: {'username': 'user1', 'shifts': ['смена1', 'смена2']},
#  2: {'username': 'user2', 'shifts': ['смена3']}}

# Функция для добавления пользователя


def add_user(user_id: int, username: str) -> None:
    if user_id not in user_database:
        user_database[user_id] = {'username': username, 'shifts': []}
        logger.info(f"Пользователь {username} добавлен с ID {user_id}")
    else:
        logger.info(f"Пользователь с ID {user_id} уже существует")

# Функция для добавления смены пользователю


def add_shift(user_id: int, shift: str) -> None:
    if user_id in user_database:
        user_database[user_id]['shifts'].append(shift)
        logger.info(f"Смена {shift} добавлена пользователю с ID {user_id}")
    else:
        logger.info(f"Пользователь с ID {user_id} не найден")
