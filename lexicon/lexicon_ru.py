# текст который пишет бота
LEXICON_RU: dict[str, str] = {
    # "other": "простите, я вас не понимаю",
    # "main_menu_junior": "Добро пожаловать, оператор, "
    #                     "выберите интересующую вас опцию",
    # "schedule": "выберете интересующую дату",
    "user_not_in_system": "Не можем обнаружит вас в системе, обратитесь к тех."
                          "специалисту или руководителю ❤",
    # "enter_username": "Пожалуйста введите свое имя\n"
    #                   "Имя должно состоять полностью из букв",
    # "entered_not_username": "Данное имя не подходит, "
    #                         "оно содержит не только буквы\n\n"
    #                         "Пожалуйста введите свое имя\n"
    #                         "Имя должно состоять полностью из букв",
    # "enter_emoji": "Имя принято.\n\n"
    #                   "Пожалуиста, отправьте эмодзи из классического набора.\n"
    #                   "Если стикер будет добавлен из Telegram Premium,"
    #                   "то он будет автоматически отформатирован.\n"
    #                   "Эмодзи нужно отправить без дополнительных символов\n"
    #                   "В дальнейшем можно всегда заменить эмодзи",
    # "entered_not_emoji": "Вы допустили ошибку, при вводе эмодзи\n\n"
    #                         "Пожалуйста, отправьте только эмодзи\n"
    #                         "Например: 🙈",
    # "registration_done": "Регистрация успешно выполнена\n\n",
    # "busy_emoji": "Данное эмодзи уже занято, выберете,"
    #               "то которое не входит в данный список\n\n",
    "schedule_type": "Выберите тип расписания:",
    # "start": "🟩 Начал",
    # "end": "🟥 Закончил",
    # 'select_shift_when_fill_report': "Пожалуйста выберите страницу и дату смены",
    # "send_photo": "Отправьте фото для\n",
    # "is_that_correct": "Проверьте, верны ли данные перед отправкой",
    # "send_report_to_topik": "Заработано",
    # "report_is_right_or_not": "Проверьте отчет, и если все верно, подтвердите",
    # "report_is_right": "Отчет подтвержден",
    # "waiting_for_payment": "Ожидает оплаты \n",
    # "select_days": "Выберите даты на которые выйдете",
    # "shifts_is_apply": "Смены проставлены",
    "shifts_is_not_apply": "Некоторые смены обновились, проверьте еще раз и подтвердите"

}

# текст которым реагируют команды
LEXICON_COMMANDS_RU: dict[str, str] = {
    # "/start": "привет!",
    # "/help": "помогу если пойму как",
}

# описание команд
LEXICON_COMMANDS_DESC_RU: dict[str, str] = {
    "/start": "команда start",
    "/help": "может помогать, но пока не умеет",
}

# текст для кнопок
LEXICON_BUTTON_RU: dict[str, str] = {
    "back": "назад!",
    "not_in_the_system": "еще не в системе?",
    "in_the_system": "Уже в системе?",
    "check_in": "Зайти на смену🕳",
    "clock_out": "выйти со смены👌",
    "write_a_report": "написать отчёт✅",
    "schedule": "Расписание📆",
    "my_money": "мои деньги💸",
    "user_not_in_system": "‼",
    "busy_emojis": "Посмотреть занятые эмодзи",
    "month_schedule": "Расписание по месяцам",
    "week_schedule": "Расписание по неделям",
}

LEXICON_ROLES_RU: dict[str, str] = {
    #     "junior": "оператор",
    #     "senior": "старший оператор",
    #     "head": "руководитель"
}
