# текст который пишет бота
LEXICON_RU: dict[str, str] = {
    'other': 'простите, я вас не понимаю',
    'main_menu_junior': 'Добро пожаловать, секстер, '
    'выберите интересующую вас опцию',
    'schedule': 'выберете интересующую дату',
    'user_not_in_system': 'Не можем обнаружит вас в системе, обратитесь к тех.'
    'специалисту или руководителю ❤',
    'enter_username': 'Пожалуйста введите свое имя\n'
    'Имя должно состоять полностью из букв',
    'entered_not_username': 'Данное имя не подходит, '
    'оно содержит не только буквы\n\n',
    'enter_emoticon': 'Имя принято.\n\n'
    'Пожалуста, отправьте эмодзи из классического набора.\n'
    'Если стикер будет добавлен из Telegram Premium,'
    'то он будет автоматически отформатирован.\n'
    'Эмодзи нужно отправить без дополнительных символов\n'
    'В дальнейшем можно всегда заменить эмодзи',
    'entered_not_emoticon': 'Вы допустили ошибку, при вводе эмоджи\n\n'
    'Пожалуйста, потправьте только эмоджи\n'
    'Например: 🙈',
    'registration_done': 'Регистрация успешно выполнена\n\n'
}

# текст которым реагируют команды
LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'привет!',
    '/help': 'помогу если пойму как'
}

# описание команд
LEXICON_COMMANDS_DESC_RU: dict[str, str] = {
    '/start': 'команда start',
    '/help': 'может помогать, но пока не умеет'
}

# текст для кнопок
LEXICON_BUTTON_RU: dict[str, str] = {
    'back': 'назад!',
    'not_in_the_system': 'еще не в системе?',
    'in_the_system': 'Уже в системе?',
    'check_in': 'Зайти на смену🕳',
    'clock_out': 'выйти со смены👌',
    'write_a_report': 'написать отчёт✅',
    'schedule': 'Расписание📆',
    'my_money': 'мои деньги💸',
    'model_statistics': 'статистика модели🎢',
    'training_materials': 'обучающие материалы📖',
    'user_not_in_system': '‼',
    'busy_emojis': 'Посмотреть занятые эмодзи'

}

LEXICON_MODELS_RU: dict[str, str] = {
    'Kate': 'Катя',
    'Caroline':  'Каролина',
    'Tanya_free': 'Таня_free',
    'Tanya_vip': 'Таня_vip',
    'Vika': 'Вика',
    'Odina': 'Одина',
    'Elly': 'Элли',
    'Lora': 'Лора',
    'Alina': 'Алина'

}

LEXICON_SHIFTS_RU: dict[str, str] = {
    '0_6': '00:00-06:00',
    '6_12': '6:00-12:00',
    '12_18': '12:00-18:00',
    '18_0': '18:00-00:00'
}

LEXICON_SCHEDULE_RU: dict[str, str] = {
    'pre_model': '<<<',
    'next_model': '>>>',
    'pre_year': '<<',
    'next_year': '>>',
    'pre_month': '<',
    'next_month': '>',
    'monday': 'Пн',
    'tuesday': 'Вт',
    'wednesday': 'Ср',
    'thursday': 'Чт',
    'friday': 'Пт',
    'saturday': 'Сб',
    'sunday': 'Вс',
    'today': 'Сегодня'
}
