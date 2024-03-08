from os import getenv
from pathlib import Path

from pydantic import BaseModel, SecretStr, PostgresDsn
from yaml import load

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


# Основной класс настроек
class Settings(BaseModel):
    bot_token: SecretStr
    db_url: PostgresDsn


# Функция, которая читает YAML-файл, валидирует и создаёт объект Settings
def parse_settings(
        local_file_name: str = "settings.yml",
) -> Settings:
    # Если задана переменная окружения BOT_CONFIG_PATH,
    # то читать будем оттуда
    file_path = getenv("BOT_CONFIG_PATH")
    if file_path is not None:
        if not Path(file_path).is_file():
            raise ValueError(
                "Path %s is not a file or doesn't exist", file_path)

    # В противном случае ищем рядом с config_reader.py файл <local_file_name>
    else:
        parent_dir = Path(__file__).parent
        settings_file = Path(
            Path.joinpath(
                parent_dir,
                local_file_name,
            )
        )
        if not Path(settings_file).is_file():
            raise ValueError(
                "Path %s is not a file or doesn't exist", settings_file)
        file_path = settings_file.absolute()
    with open(
            file_path,
            "rt",
    ) as file:
        config_data = load(
            file,
            SafeLoader,
        )
    # После прочтения файла накладываем его на
    # модель и получаем объект Settings
    return Settings.model_validate(config_data)


settings = parse_settings()
