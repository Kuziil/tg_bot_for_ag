import datetime as dt
import logging
from calendar import monthcalendar, monthrange, day_abbr
from typing import Any
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from callback_factories.back import BackCallbackData
from db.models import (
    PagesORM,
    PagesIntervalsORM,
    IntervalsORM,
    UsersORM,
    TgsORM,
    ShiftsORM,
)
from db.requests.with_page import (
    get_pages_by_user_tg_id,
)
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthScheduleCallbackData,
)
from keyboards.schedule.month_v2.creators_row import (
    create_row_intervals,
    create_row_lineups,
    create_row_month_year,
    create_row_pages,
)

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

logger = logging.getLogger(__name__)


async def process_datetime(
        default_tz: ZoneInfo,
        current_day: int | None,
        current_month: int | None,
        current_year: int | None,
) -> dict[str, dt.datetime]:
    dict_datetimes: dict[str, dt.datetime] = {}
    current_datetime_now: dt.datetime = dt.datetime.now(tz=default_tz)
    if current_year is None or current_month is None or current_day is None:
        current_datetime: dt.datetime = current_datetime_now
    else:
        if current_day == 0:
            current_datetime = dt.datetime(
                year=current_year,
                month=current_month,
                day=current_datetime_now.day,
                tzinfo=default_tz,
            )
        else:
            current_datetime = dt.datetime(
                year=current_year,
                month=current_month,
                day=current_day,
                tzinfo=default_tz,
            )

    dict_datetimes["current"] = current_datetime
    timedelta_of_days_for_current_month: dt.timedelta = dt.timedelta(
        days=monthrange(
            year=dict_datetimes["current"].year,
            month=dict_datetimes["current"].month,
        )[1]
    )
    dict_datetimes["before"] = (
            dict_datetimes["current"] - timedelta_of_days_for_current_month
    )
    dict_datetimes["after"] = (
            dict_datetimes["current"] + timedelta_of_days_for_current_month
    )
    return dict_datetimes


async def in_circle(
        values: list[Any],
        current: int,
):
    dict_position: dict[str, Any] = {"current": values[current]}
    len_values: int = len(values)
    if len_values == 1:
        return dict_position
    if current == 0:
        dict_position["before"] = values[-1]
        dict_position["after"] = values[current + 1]
    elif current == len_values - 1:
        dict_position["before"] = values[current - 1]
        dict_position["after"] = values[0]
    else:
        dict_position["before"] = values[current - 1]
        dict_position["after"] = values[current + 1]
    return dict_position


async def process_page(
        pages: list[PagesORM],
        current_page_id: int,
) -> dict[str, PagesORM]:
    current: int = 0
    for key, page in enumerate(pages):
        page: PagesORM = page
        if page.id == current_page_id:
            current = key
            break
    return await in_circle(values=pages, current=current)


async def create_dict_lineups(
        lineups: list[int],
        current_lineup: int,
) -> dict[str, int]:
    lineups.sort()
    current_lineup_key = current_lineup - 1

    dict_lineups: dict[str, int] = await in_circle(
        values=lineups,
        current=current_lineup_key,
    )
    return dict_lineups


async def is_dict_in_list(dictionary, list_of_dicts):
    for d in list_of_dicts:
        if (
                d["day"] == dictionary["day"]
                and d["month"] == dictionary["month"]
                and d["year"] == dictionary["year"]
                and d["page_interval_id"] == dictionary["page_interval_id"]
        ):
            return True
    return False


async def process_intervals_lineups_emojis(
        current_interval_id: int | None,
        current_lineup: int | None,
        pages_intervals: list[PagesIntervalsORM],
        user_tg_id: int,
        st_shifts: list[dict[str, str]] | None,
):
    """_summary_

    Args:
        current_interval_id (int | None): данный параметр = None
        если расписание только открыли,
        в ином случае указывает на то какой интервал отобразить

        current_lineup (int | None): данный параметр = None
        если расписание только открыли,
        в ином случае указывает на то какой состав отобразить

        pages_intervals (list[PagesIntervalsORM]):
        список всех PagesIntervalsORM которые доступны Pages,
        в которых есть текущий пользователь
        user_tg_id (int): телеграмм id пользователя
        st_shifts (list[dict[str, str]] | None):
        список смен которые наполняются с помощью FSM

    Returns:
        tuple[dict[str, IntervalsORM], dict[str, int], dict[int, str]]:
        _description_
    """
    # список с упорядоченными уникальными интервалами
    intervals: list[IntervalsORM] = []
    # список с уникальными составами
    lineups: list[int] = []
    # словарь с днями и соответствующими им эмодзи для отображения в расписании
    list_of_dict_shifts: list[dict[str, str | int]] = []
    # указатель на то что days_emojis упакован
    shifts_packed: bool = False
    # ключ интервала в intervals который отобразить
    current_interval_key: int | None = None
    current_user: UsersORM | None = None

    available_pages_intervals_id: list[int] = []

    current_page_interval_id: str | None = None

    for page_interval in pages_intervals:
        # интервал в данном page_interval
        interval: IntervalsORM = page_interval.interval
        # состав в данном page_interval
        lineup: int = page_interval.lineup
        # пользователь в данном page_interval
        user: UsersORM = page_interval.user

        # Сбор уникальных ORM интервалов
        if interval not in intervals:
            intervals.append(interval)

        # Сбор уникальных составов
        if lineup not in lineups:
            lineups.append(lineup)
        # если существует current_interval_id и current_lineup,
        # то сравнивать их с текущими значениями
        # это сделано, для того
        # чтобы получать новые current_interval_key после первой инициализации
        if (
                current_interval_id
                and current_lineup
                and interval.id == current_interval_id
                and lineup == current_lineup
        ):
            current_page_interval_id = page_interval.id
            current_interval_key = len(intervals) - 1
            current_lineup = lineup

        # Проверка на присутствие user в данном page_interval, это нужно
        # т.к. не у каждого page_interval может быть пользователь,
        # например в случае открытия новой страницы или увольнения пользователя
        if user is not None:
            # получаем список TgsORM, если пользователь существует,
            # Пользователь не может существовать без TgsORM так и
            # TgsORM не может существовать без пользователя
            # TODO: указать данное условие в ORM
            tgs: list[TgsORM] = user.tgs
            # Т.к. у пользователя может быть несколько TgsORM,
            # то проходимся по каждому
            for tg in tgs:
                # Ищем тот id, который будет совпадать
                if tg.user_tg_id == user_tg_id:
                    # Если он нашелся, то записываем его в current_user
                    current_user = user
                    available_pages_intervals_id.append(page_interval.id)
                    # если значения по умолчанию не были переданы,
                    # следовательно, это первый запуск расписания,
                    # то передаем заполняем
                    # current_interval_key и current_lineup
                    if current_interval_id is None and current_lineup is None:
                        current_page_interval_id = page_interval.id
                        current_interval_key = len(intervals) - 1
                        current_lineup = lineup
        # Данная проверка нужна, для того чтобы паковать days_emojis
        # в момент когда определен нужный интервал,
        # а также состав и соответственно страница
        if (
                current_interval_key is not None
                and current_lineup is not None
                and shifts_packed is False
        ):
            shifts: list[ShiftsORM] = page_interval.shifts
            # перебор всех смен для данной page_interval,
            # где определен current_interval_key, а так же состав
            for shift in shifts:
                # наполняем days_emojis днем и соответствующим ему эмодзи
                # для отображения в расписании
                dict_shift: dict[str, str | int] = {"day": shift.date_shift.day, "month": shift.date_shift.month,
                                                    "year": shift.date_shift.year,
                                                    "page_interval_id": shift.page_interval_id}
                # если пользователь существует и у смены нет замены,
                # то выведется эмодзи пользователя, чья смена сейчас
                if shift.replacement_id is None and user is not None:
                    dict_shift["emoji"] = user.emoji
                # если же замена указана, то выведется эмодзи замены,
                # для данной смены
                elif shift.replacement_id is not None:
                    dict_shift["emoji"] = shift.replacement.emoji
                list_of_dict_shifts.append(dict_shift)
            shifts_packed = True

    # в данной проверке оценивается, был ле передан st_shifts,
    # для того чтобы в дальнейшем отобразить смены на расписании
    if st_shifts is not None and current_user is not None:

        # данный цикл нужен для отображения новых данных, до отправки их в бд
        for st_shift in st_shifts:
            if (
                    not await is_dict_in_list(
                        dictionary=st_shift, list_of_dicts=list_of_dict_shifts
                    )
                    and st_shift["page_interval_id"]
                    in available_pages_intervals_id
            ):
                dict_shift_from_st = {
                    "day": st_shift["day"],
                    "month": st_shift["month"],
                    "year": st_shift["year"],
                    "page_interval_id": st_shift["page_interval_id"],
                    "emoji": "🟢"
                }
                list_of_dict_shifts.append(dict_shift_from_st)
            else:
                st_shifts.remove(st_shift)
        logger.debug(f"st_shifts: {st_shifts}")

    dict_intervals: dict[str, IntervalsORM] = await in_circle(
        values=intervals,
        current=current_interval_key,
    )
    dict_lineups: dict[str, int] = await create_dict_lineups(
        lineups=lineups,
        current_lineup=current_lineup,
    )
    return (
        dict_intervals,
        dict_lineups,
        list_of_dict_shifts,
        st_shifts,
        current_page_interval_id,
    )


async def create_month_schedule_v2(
        user_tg_id: int,
        session: AsyncSession,
        default_tz: ZoneInfo,
        i18n: TranslatorRunner,
        current_page_id: int | None = None,
        current_year: int | None = None,
        current_month: int | None = None,
        current_day: int | None = None,
        current_interval_id: int | None = None,
        current_lineup: int | None = None,
        st_shifts: list[dict[str, str]] | None = None,
):
    kb_builder = InlineKeyboardBuilder()
    dict_datetimes: dict[str, dt.datetime] = await process_datetime(
        default_tz=default_tz,
        current_day=current_day,
        current_month=current_month,
        current_year=current_year,
    )
    pages: list[PagesORM] = await get_pages_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
        current_month=dict_datetimes["current"].month,
    )
    # NOTE: в pages, находятся только те смены которые
    # соответствуют переданному месяцу
    pages = sorted(pages, key=lambda x: (x.model.title, x.type_in_agency))
    # for page_t in pages:
    #     logger.debug(f"{page_t}")
    #     logger.debug(f"    {page_t.model}")
    #     for page_interval_t in page_t.intervals_details:
    #         logger.debug(f"    {page_interval_t}")
    #         logger.debug(f"    {page_interval_t.interval}")
    #         logger.debug(f"    {page_interval_t.user}")
    #         if page_interval_t.user is not None:
    #             for tgs_t in page_interval_t.user.tgs:
    #                 logger.debug(f"        {tgs_t}")
    #         else:
    #             logger.debug(f"            None")

    #         for shift_t in page_interval_t.shifts:
    #             logger.debug(f"        {shift_t}")
    #             if shift_t.replacement_id is not None:
    #                 logger.debug(f"           {shift_t.replacement.emoji}")
    dict_pages: dict[str, PagesORM] = await process_page(
        pages=pages,
        current_page_id=current_page_id,
    )

    page: PagesORM = dict_pages["current"]
    pages_intervals: list[PagesIntervalsORM] = sorted(
        page.intervals_details,
        key=lambda x: x.interval.start_at,
    )

    dict_intervals_and_lineups = await process_intervals_lineups_emojis(
        current_interval_id=current_interval_id,
        current_lineup=current_lineup,
        pages_intervals=pages_intervals,
        user_tg_id=user_tg_id,
        st_shifts=st_shifts,
    )

    dict_intervals: dict[str, IntervalsORM] = dict_intervals_and_lineups[0]
    dict_lineups: dict[str, int] = dict_intervals_and_lineups[1]
    dict_days_emojis: list[dict[str, str | int]] = dict_intervals_and_lineups[2]
    st_shifts: list[dict[str, str]] = dict_intervals_and_lineups[3]
    current_page_interval_id: int = dict_intervals_and_lineups[4]

    # row month_year
    kb_builder.row(
        *await create_row_month_year(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
            current_page_interval_id=current_page_interval_id,
            i18n=i18n,
            st_shifts=st_shifts,
        )
    )
    # row weekday
    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=weekday,
                callback_data=MonthScheduleCallbackData(
                    day=0,
                    month=dict_datetimes["current"].month,
                    year=dict_datetimes["current"].year,
                    page_id=dict_pages["current"].id,
                    lineup=dict_lineups["current"],
                    interval_id=dict_intervals["current"].id,
                    page_interval_id=current_page_interval_id,
                    apply=0,
                ).pack(),
            )
            for weekday in day_abbr
        ]
    )

    # row days
    month_calendar: list[list[int]] = monthcalendar(
        year=dict_datetimes["current"].year,
        month=dict_datetimes["current"].month,
    )
    for week in month_calendar:
        week_ikb: list[InlineKeyboardButton] = []
        for day in week:
            if day > 0:
                day_str = f"{day}"
                for dict_shift in dict_days_emojis:
                    d_s_month = dict_shift["month"]
                    d_s_year = dict_shift["year"]
                    d_s_day = dict_shift["day"]
                    d_s_page_interval_id = dict_shift["page_interval_id"]
                    if (
                            d_s_day == day
                            and d_s_month == dict_datetimes["current"].month
                            and d_s_year == dict_datetimes["current"].year
                            and d_s_page_interval_id == current_page_interval_id
                    ):
                        day_str = dict_shift["emoji"]
                        break
            else:
                day_str = " "

            week_ikb.append(
                InlineKeyboardButton(
                    text=i18n.button.day(day=day_str),
                    callback_data=MonthScheduleCallbackData(
                        day=day,
                        month=dict_datetimes["current"].month,
                        year=dict_datetimes["current"].year,
                        page_id=dict_pages["current"].id,
                        lineup=dict_lineups["current"],
                        interval_id=dict_intervals["current"].id,
                        page_interval_id=current_page_interval_id,
                        apply=0,
                    ).pack(),
                )
            )
        kb_builder.row(*week_ikb)

    # row lineup
    if "before" in dict_lineups and "after" in dict_lineups:
        kb_builder.row(
            *await create_row_lineups(
                dict_datetimes=dict_datetimes,
                dict_pages=dict_pages,
                dict_lineups=dict_lineups,
                dict_intervals=dict_intervals,
                current_page_interval_id=current_page_interval_id,
                i18n=i18n,
                st_shifts=st_shifts,
            )
        )
    # row page
    kb_builder.row(
        *await create_row_pages(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
            current_page_interval_id=current_page_interval_id,
            i18n=i18n,
            st_shifts=st_shifts,
        )
    )
    # row interval
    kb_builder.row(
        *await create_row_intervals(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
            default_tz=default_tz,
            current_page_interval_id=current_page_interval_id,
            i18n=i18n,
            st_shifts=st_shifts,
        )
    )

    if st_shifts:
        kb_builder.row(
            InlineKeyboardButton(
                text=i18n.button.cancel(),
                callback_data=MonthScheduleCallbackData(
                    day=0,
                    month=dict_datetimes["current"].month,
                    year=dict_datetimes["current"].year,
                    page_id=dict_pages["current"].id,
                    lineup=dict_lineups["current"],
                    interval_id=dict_intervals["current"].id,
                    page_interval_id=current_page_interval_id,
                    apply=2,
                ).pack(),
            ),
            InlineKeyboardButton(
                text=i18n.button.apply(),
                callback_data=MonthScheduleCallbackData(
                    day=0,
                    month=dict_datetimes["current"].month,
                    year=dict_datetimes["current"].year,
                    page_id=dict_pages["current"].id,
                    lineup=dict_lineups["current"],
                    interval_id=dict_intervals["current"].id,
                    page_interval_id=current_page_interval_id,
                    apply=1,
                ).pack(),
            ),
        )
        return kb_builder.as_markup(), st_shifts
    else:
        kb_builder.row(
            InlineKeyboardButton(
                text=i18n.button.back(),
                callback_data=BackCallbackData(
                    handler="process_schedule_press",
                ).pack(),
            ),
            InlineKeyboardButton(
                text=i18n.button.update(),
                callback_data=MonthScheduleCallbackData(
                    day=0,
                    month=dict_datetimes["current"].month,
                    year=dict_datetimes["current"].year,
                    page_id=dict_pages["current"].id,
                    lineup=dict_lineups["current"],
                    interval_id=dict_intervals["current"].id,
                    page_interval_id=current_page_interval_id,
                    apply=0,
                ).pack(),
            ),
        )
        return kb_builder.as_markup()
