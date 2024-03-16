from typing import Literal


class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...

    text: Text
    caption: Caption
    button: Button


class Text:
    other: TextOther
    main: TextMain
    not_in_agency: TextNot_in_agency
    in_agency: TextIn_agency
    report: TextReport
    month: TextMonth


class TextOther:
    @staticmethod
    def no() -> Literal["""Простите, я вас не понимаю"""]: ...


class TextMain:
    name: TextMainName

    @staticmethod
    def menu(*, userEmoji, userName) -> Literal["""Приветствую, { $userEmoji } { $userName }.
Выберите интересующую опцию"""]: ...

    @staticmethod
    def select_in_or_not() -> Literal["""Вы уже в агентстве или нет?"""]: ...

    @staticmethod
    def help() -> Literal["""Может помогать, но пока не умеет"""]: ...


class TextMainName:
    @staticmethod
    def fill() -> Literal["""Пожалуйста введите свое имя
Имя должно состоять полностью из букв"""]: ...


class TextNot_in_agency:
    name: TextNot_in_agencyName
    emoji: TextNot_in_agencyEmoji


class TextNot_in_agencyName:
    sent: TextNot_in_agencyNameSent


class TextNot_in_agencyNameSent:
    @staticmethod
    def __call__() -> Literal["""Имя принято

Пожалуйста, отправьте эмодзи из классического набора.
Если стикер будет добавлен из Telegram Premium, то он будет автоматически отформатирован.
Эмодзи нужно отправить без дополнительных символов.
В дальнейшем можно всегда заменить эмодзи."""]: ...

    @staticmethod
    def wrong() -> Literal["""Данное имя не подходит, оно содержит не только буквы.

Пожалуйста введите свое имя.
Имя должно состоять полностью из букв."""]: ...


class TextNot_in_agencyEmoji:
    sent: TextNot_in_agencyEmojiSent

    @staticmethod
    def example() -> Literal["""🙈"""]: ...


class TextNot_in_agencyEmojiSent:
    @staticmethod
    def __call__() -> Literal["""Регистрация успешно выполнена."""]: ...

    @staticmethod
    def busy() -> Literal["""Данное эмодзи уже занято, выберете, то которое не входит в данный список"""]: ...

    @staticmethod
    def wrong() -> Literal["""Вы допустили ошибку, при вводе эмодзи.

Пожалуйста, отправьте только эмодзи.

Например:"""]: ...


class TextIn_agency:
    my_money: TextIn_agencyMy_money

    @staticmethod
    def schedule() -> Literal["""Выберете интересующую дату."""]: ...

    @staticmethod
    def check_in(*, userEmoji, userName) -> Literal["""Вы вышли на смену, удачи, { $userEmoji } { $userName }!"""]: ...

    @staticmethod
    def check_in_or_clock_out(*, userEmoji, userTgId, userName, formattedDate) -> Literal["""{ $userEmoji }&lt;a href=&#34;tg://user?id={ $userTgId }&#34;&gt;{ $userName }&lt;/a&gt;

&lt;b&gt;{ $formattedDate }&lt;/b&gt;"""]: ...

    @staticmethod
    def clock_out() -> Literal["""Вы вышли со смены, не забудьте заполнить отчет!"""]: ...

    @staticmethod
    def write_a_report() -> Literal["""Пожалуйста выберите страницу и дату смены."""]: ...


class TextIn_agencyMy_money:
    @staticmethod
    def head() -> Literal["""Ожидает оплаты:
"""]: ...

    @staticmethod
    def body(*, pageTitle, totalDirtyEarnings) -> Literal["""{ $pageTitle }: { $totalDirtyEarnings }$
"""]: ...


class TextReport:
    photos: TextReportPhotos
    media: TextReportMedia
    thread: TextReportThread

    @staticmethod
    def sent() -> Literal["""Отчет успешно отправлен."""]: ...


class TextReportPhotos:
    @staticmethod
    def fill(*, day, month, year) -> Literal[
        """Отправьте фото для\nсмены прошедшей { $day }.{ $month }.{ $year }"""]: ...


class Caption:
    report: CaptionReport


class CaptionReport:
    thread: CaptionReportThread

    @staticmethod
    def dirty(*, dirty) -> Literal["""{ $dirty }$"""]: ...


class TextReportMedia:
    @staticmethod
    def check() -> Literal["""Проверьте, верны ли данные перед отправкой."""]: ...


class CaptionReportThread:
    @staticmethod
    def correct(*, dirty) -> Literal["""Заработано - { $dirty }"""]: ...


class TextReportThread:
    @staticmethod
    def check() -> Literal["""Проверьте отчет, и если все верно, подтвердите."""]: ...

    @staticmethod
    def confirmed() -> Literal["""Отчет подтвержден."""]: ...


class TextMonth:
    shifts: TextMonthShifts

    @staticmethod
    def __call__() -> Literal["""Выберите даты на которые выйдете."""]: ...


class TextMonthShifts:
    @staticmethod
    def well() -> Literal["""Смены проставлены."""]: ...

    @staticmethod
    def badly() -> Literal["""Некоторые смены обновились, проверьте еще раз и подтвердите."""]: ...


class Button:
    curly: ButtonCurly
    model: ButtonModel
    page: ButtonPage

    @staticmethod
    def cancel() -> Literal["""Отменить"""]: ...

    @staticmethod
    def apply() -> Literal["""Применить"""]: ...

    @staticmethod
    def back() -> Literal["""Назад"""]: ...

    @staticmethod
    def update() -> Literal["""Обновить"""]: ...

    @staticmethod
    def month(*, month) -> Literal["""{ $month }"""]: ...

    @staticmethod
    def year(*, year) -> Literal["""{ $year }"""]: ...

    @staticmethod
    def time(*, time) -> Literal["""{ $time }"""]: ...

    @staticmethod
    def lineup(*, lineup) -> Literal["""{ $lineup }"""]: ...

    @staticmethod
    def day(*, day) -> Literal["""{ $day }"""]: ...


class ButtonCurly:
    @staticmethod
    def back() -> Literal["""&lt;"""]: ...

    @staticmethod
    def forward() -> Literal["""&gt;"""]: ...


class ButtonModel:
    @staticmethod
    def title(*, modelTitle) -> Literal["""{ $modelTitle }"""]: ...


class ButtonPage:
    @staticmethod
    def type_in_agency(*, typeInAgency) -> Literal["""{ $typeInAgency }"""]: ...


class ButtonLineup:
    @staticmethod
    def title() -> Literal["""Состав:"""]: ...
