text-other-no = Простите, я вас не понимаю

text-main-menu =
    Приветствую, {$userEmoji}{$userRole ->
        *[junior] оператор
        [senior] старший
        [head]  руководитель
    } {$userName}.
    Выберите интересующую опцию

text-main-select_in_or_not =
    Вы уже в агентстве или нет?

text-main-help =
    Может помогать, но пока не умеет

text-main-name-fill =
    Пожалуйста введите свое имя
    Имя должно состоять полностью из букв

text-not_in_agency-name-sent =
    Имя принято

    Пожалуйста, отправьте эмодзи из классического набора.
    Если стикер будет добавлен из Telegram Premium, то он будет автоматически отформатирован.
    Эмодзи нужно отправить без дополнительных символов.
    В дальнейшем можно всегда заменить эмодзи.

text-not_in_agency-name-sent-wrong =
    Данное имя не подходит, оно содержит не только буквы.

    Пожалуйста введите свое имя.
    Имя должно состоять полностью из букв.

text-not_in_agency-emoji-sent =
    Регистрация успешно выполнена.

text-not_in_agency-emoji-sent-busy =
    Данное эмодзи уже занято, выберете, то которое не входит в данный список

text-not_in_agency-emoji-sent-wrong =
    Вы допустили ошибку, при вводе эмодзи.

    Пожалуйста, отправьте только эмодзи.

    Например:

text-not_in_agency-emoji-example =
    🙈

text-in_agency-schedule =
    Выберете интересующую дату.

text-in_agency-check_in =
    Вы вышли на смену, удачи, {$userEmoji}{$userRole ->
        *[junior] оператор
        [senior] старший
        [head]  руководитель
    } {$userName}!

text-in_agency-check_in_or_clock_out =
    {$userEmoji}<a href="tg://user?id={$userTgId}">{$userName}</a>
    {$checkInOrClockOut ->
        *[clock_out] 🟥 Закончил
        [check_in] 🟩 Начал смену
    }
    <b>{$formattedDate}</b>

text-in_agency-clock_out =
    Вы вышли со смены, не забудьте заполнить отчет!

text-in_agency-write_a_report =
    Пожалуйста выберите страницу и дату смены.

text-in_agency-my_money-head =
    Ожидает оплаты:
    {""}

text-in_agency-my_money-body =
    {$pageTitle}: {$totalDirtyEarnings}$
    {""}


text-report-photos-fill =
    Отправьте фото для\nсмены прошедшей {$day}.{$month}.{$year}

caption-report-dirty =
    {$dirty}$

text-report-media-check =
    Проверьте, верны ли данные перед отправкой.

caption-report-thread-correct =
    Заработано - {$dirty}

text-report-thread-check =
    Проверьте отчет, и если все верно, подтвердите.

text-report-sent =
    Отчет успешно отправлен.

text-report-thread-confirmed =
    Отчет подтвержден.

text-month =
    Выберите даты на которые выйдете.

text-month-shifts-well =
    Смены проставлены.

text-month-shifts-badly =
    Некоторые смены обновились, проверьте еще раз и подтвердите.

button-cancel =
    Отменить

button-apply =
    Применить

button-back =
    Назад

button-update =
    Обновить

button-curly-back  =
    <

button-curly-forward  =
    >

button-month =
    {$month}

button-year =
    {$year}

button-model-title =
    {$modelTitle}

button-page-type_in_agency =
    {$typeInAgency}

button-time =
    {$time}

button-lineup-title =
    Состав:

button-lineup =
    {$lineup}

button-day =
    {$day}

text-statistic-select-page =
    Выберите страницу по которой хотите посмотреть статистику

button-statistic-page =
    {$pageTitle}
