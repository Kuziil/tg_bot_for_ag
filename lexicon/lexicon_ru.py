# текст который пишет бота
LEXICON_RU: dict[str, str] = {
    'other': 'простите, я вас не понимаю',
    'main_menu_junior': 'Добро пожаловать, секстер, '
    'выберите интересующую вас опцию',
    'schedule': 'выберете интересующую дату'
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
    'training_materials': 'обучающие материалы📖'

}

LEXICON_MODELS_RU: dict[str, str] = {
    'Kate': 'Катя',
    'Tanya': 'Таня'
}

LEXICON_SHIFTS_RU: dict[str, str] = {
    '0-6': '00:00-06:00',
    '6-12': '6:00-12:00',
    '12-18': '12:00-18:00',
    '18-0': '18:00-00:00'
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
