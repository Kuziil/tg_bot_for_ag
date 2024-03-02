import datetime as dt
from calendar import monthcalendar, monthrange, day_abbr
from typing import Any
from zoneinfo import ZoneInfo
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from db.requests.with_page import (
    get_pages_with_inter_users_tgs_shifts_by_user_tg_id,
)
from db.requests.with_add import add_shift
from db.models import (
    PagesORM,
    PagesIntervalsORM,
    IntervalsORM,
    UsersORM,
    TgsORM,
    ModelsORM,
    ShiftsORM,
)
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthShudleCallbackData,
)

logger = logging.getLogger(__name__)


async def process_datetime(
    defult_tz: ZoneInfo,
    current_day: int | None,
    current_month: int | None,
    current_year: int | None,
) -> dict[str, dt.datetime]:
    dict_datetimes: dict[str, dt.datetime] = {}
    current_datetime_now: dt.datetime = dt.datetime.now(tz=defult_tz)
    if current_year is None or current_month is None or current_day is None:
        current_datetime: dt.datetime = current_datetime_now
    else:
        current_datetime: dt.datetime = None
        if current_day == 0:
            current_datetime = dt.datetime(
                year=current_year,
                month=current_month,
                day=current_datetime_now.day,
                tzinfo=defult_tz,
            )
        else:
            current_datetime = dt.datetime(
                year=current_year,
                month=current_month,
                day=current_day,
                tzinfo=defult_tz,
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
    dict_position: dict[str, Any] = {}
    dict_position["current"] = values[current]
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


async def convert_datetime_to_time_str(
    defult_tz: ZoneInfo,
    time: dt.datetime,
) -> str:
    time_str: str = time.astimezone(defult_tz).strftime("%H:%M")
    return time_str


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


async def process_intervals_lineups_emojis(
    session: AsyncSession,
    current_interval_id: int | None,
    current_lineup: int | None,
    current_datetime: dt.datetime | None,
    current_day: int | None,
    pages_intervals: list[PagesIntervalsORM],
    user_tg_id: int,
    st_shifts: list[dict[str, str]] | None,
) -> tuple[dict[str, IntervalsORM], dict[str, int], dict[int, str]]:

    intervals: list[IntervalsORM] = []
    current_user: UsersORM = None
    lineups: list[int] = []
    current_interval_key: int | None = None
    days_emojis: dict[int, str] = {}
    shifts_packed: bool = False

    for page_interval in pages_intervals:
        interval: IntervalsORM = page_interval.interval
        lineup: int = page_interval.lineup
        user: UsersORM = page_interval.user

        if interval not in intervals:
            intervals.append(interval)

        if lineup not in lineups:
            lineups.append(lineup)

        if user is not None:
            tgs: list[TgsORM] = user.tgs

            for tg in tgs:

                if tg.user_tg_id == user_tg_id:
                    current_user = user

                    if current_interval_id is None and current_lineup is None:
                        current_interval_key = len(intervals) - 1
                        current_lineup = lineup

        if (
            current_interval_id
            and current_lineup
            and interval.id == current_interval_id
            and lineup == current_lineup
        ):
            current_interval_key = len(intervals) - 1

        if current_interval_key is not None and shifts_packed is False:
            shifts: list[ShiftsORM] = page_interval.shifts

            for shift in shifts:

                if shift.replacement_id is None and user is not None:
                    days_emojis[shift.date_shift.day] = user.emoji

                else:
                    days_emojis[shift.date_shift.day] = shift.replacement.emoji

            if (
                current_datetime is not None
                and current_day is not None
                and current_day != 0
                and current_day not in days_emojis
                and current_user == user
            ):
                current_date: dt.date = current_datetime.date()
                # await add_shift(
                #     session=session,
                #     date_shift=current_date,
                #     page_interval_id=page_interval.id,
                # )
                for st_shift in st_shifts:

                    st_day = st_shift["day"]
                    # days_emojis[st_day] = user.emoji
                    days_emojis[st_day] = "🟢"

            shifts_packed = True

    dict_intervals: dict[str, IntervalsORM] = await in_circle(
        values=intervals,
        current=current_interval_key,
    )
    dict_lineups: dict[str, int] = await create_dict_lineups(
        lineups=lineups,
        current_lineup=current_lineup,
    )
    return dict_intervals, dict_lineups, days_emojis


async def create_row_month_year(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": f"<",
        },
        {
            "sequence_item": "current",
            "text": dict_datetimes["current"].strftime("%b"),
        },
        {
            "sequence_item": "current",
            "text": f'{dict_datetimes["current"].year}',
        },
        {
            "sequence_item": "after",
            "text": f">",
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_datetimes:
            buttons.append(
                InlineKeyboardButton(
                    text=button["text"],
                    callback_data=MonthShudleCallbackData(
                        day=0,
                        month=dict_datetimes[button["sequence_item"]].month,
                        year=dict_datetimes[button["sequence_item"]].year,
                        page_id=dict_pages["current"].id,
                        lineup=dict_lineups["current"],
                        interval_id=dict_intervals["current"].id,
                        apply=0,
                    ).pack(),
                )
            )
    return buttons


async def create_row_pages(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": "<<<",
        },
        {
            "sequence_item": "current",
            "text": dict_pages["current"].model.title,
        },
        {
            "sequence_item": "current",
            "text": dict_pages["current"].type_in_agency,
        },
        {
            "sequence_item": "after",
            "text": ">>>",
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_pages:
            buttons.append(
                InlineKeyboardButton(
                    text=button["text"],
                    callback_data=MonthShudleCallbackData(
                        day=0,
                        month=dict_datetimes["current"].month,
                        year=dict_datetimes["current"].year,
                        page_id=dict_pages[button["sequence_item"]].id,
                        lineup=dict_lineups["current"],
                        interval_id=dict_intervals["current"].id,
                        apply=0,
                    ).pack(),
                )
            )
    return buttons


async def create_row_inervals(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
    defult_tz: ZoneInfo,
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": "<<<",
        },
        {
            "sequence_item": "current",
            "text": await convert_datetime_to_time_str(
                time=dict_intervals["current"].start_at,
                defult_tz=defult_tz,
            ),
        },
        {
            "sequence_item": "current",
            "text": await convert_datetime_to_time_str(
                time=dict_intervals["current"].end_at,
                defult_tz=defult_tz,
            ),
        },
        {
            "sequence_item": "after",
            "text": ">>>",
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_intervals:
            buttons.append(
                InlineKeyboardButton(
                    text=button["text"],
                    callback_data=MonthShudleCallbackData(
                        day=0,
                        month=dict_datetimes["current"].month,
                        year=dict_datetimes["current"].year,
                        page_id=dict_pages["current"].id,
                        lineup=dict_lineups["current"],
                        interval_id=dict_intervals[button["sequence_item"]].id,
                        apply=0,
                    ).pack(),
                )
            )
    return buttons


async def create_row_lineups(
    dict_datetimes: dict[str, dt.datetime],
    dict_pages: dict[str, PagesORM],
    dict_lineups: dict[str, int],
    dict_intervals: dict[str, IntervalsORM],
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": "<<<",
        },
        {
            "sequence_item": "current",
            "text": f'{dict_lineups["current"]}',
        },
        {
            "sequence_item": "after",
            "text": ">>>",
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_lineups:
            buttons.append(
                InlineKeyboardButton(
                    text=button["text"],
                    callback_data=MonthShudleCallbackData(
                        day=0,
                        month=dict_datetimes["current"].month,
                        year=dict_datetimes["current"].year,
                        page_id=dict_pages["current"].id,
                        lineup=dict_lineups[button["sequence_item"]],
                        interval_id=dict_intervals["current"].id,
                        apply=0,
                    ).pack(),
                )
            )
    return buttons


async def create_month_shudle_v2(
    user_tg_id: int,
    session: AsyncSession,
    i18n: dict[dict[str, str]],
    defult_tz: ZoneInfo,
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
        defult_tz=defult_tz,
        current_day=current_day,
        current_month=current_month,
        current_year=current_year,
    )
    pages: list[PagesORM] = await get_pages_with_inter_users_tgs_shifts_by_user_tg_id(
        session=session,
        user_tg_id=user_tg_id,
        current_month=dict_datetimes["current"].month,
    )
    pages = sorted(pages, key=lambda x: (x.model.title, x.type_in_agency))
    for page_t in pages:
        logger.debug(f"{page_t}")
        logger.debug(f"    {page_t.model}")
        for page_interval_t in page_t.intervals_details:
            logger.debug(f"    {page_interval_t}")
            logger.debug(f"    {page_interval_t.interval}")
            logger.debug(f"    {page_interval_t.user}")
            if page_interval_t.user is not None:
                for tgs_t in page_interval_t.user.tgs:
                    logger.debug(f"        {tgs_t}")
            else:
                logger.debug(f"            None")

            for shift_t in page_interval_t.shifts:
                logger.debug(f"        {shift_t}")
                if shift_t.replacement_id is not None:
                    logger.debug(f"                     {shift_t.replacement.emoji}")
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
        session=session,
        current_interval_id=current_interval_id,
        current_lineup=current_lineup,
        current_datetime=dict_datetimes["current"],
        current_day=current_day,
        pages_intervals=pages_intervals,
        user_tg_id=user_tg_id,
        st_shifts=st_shifts,
    )

    dict_intervals: dict[str, IntervalsORM] = dict_intervals_and_lineups[0]
    dict_lineups: dict[str, int] = dict_intervals_and_lineups[1]
    dict_days_emojis: dict[int, str] = dict_intervals_and_lineups[2]

    # row month_year
    kb_builder.row(
        *await create_row_month_year(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
        )
    )
    # row weekday
    kb_builder.row(
        *[
            InlineKeyboardButton(
                text=weekday,
                callback_data=MonthShudleCallbackData(
                    day=0,
                    month=dict_datetimes["current"].month,
                    year=dict_datetimes["current"].year,
                    page_id=dict_pages["current"].id,
                    lineup=dict_lineups["current"],
                    interval_id=dict_intervals["current"].id,
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
                if day in dict_days_emojis:
                    day_str = dict_days_emojis[day]
                else:
                    day_str = f"{day}"
            else:
                day_str = f" "
            week_ikb.append(
                InlineKeyboardButton(
                    text=day_str,
                    callback_data=MonthShudleCallbackData(
                        day=day,
                        month=dict_datetimes["current"].month,
                        year=dict_datetimes["current"].year,
                        page_id=dict_pages["current"].id,
                        lineup=dict_lineups["current"],
                        interval_id=dict_intervals["current"].id,
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
            )
        )
    # row page
    kb_builder.row(
        *await create_row_pages(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
        )
    )
    # row interval
    kb_builder.row(
        *await create_row_inervals(
            dict_datetimes=dict_datetimes,
            dict_pages=dict_pages,
            dict_lineups=dict_lineups,
            dict_intervals=dict_intervals,
            defult_tz=defult_tz,
        )
    )

    if st_shifts:
        kb_builder.row(
            InlineKeyboardButton(
                text="Отменить",
                callback_data="ch",
            ),
            InlineKeyboardButton(
                text="Применить",
                callback_data="ap",
            ),
        )
    else:
        kb_builder.row(
            InlineKeyboardButton(
                text="назад",
                callback_data="back_button",
            ),
            InlineKeyboardButton(
                text="обновить",
                callback_data=MonthShudleCallbackData(
                    day=0,
                    month=dict_datetimes["current"].month,
                    year=dict_datetimes["current"].year,
                    page_id=dict_pages["current"].id,
                    lineup=dict_lineups["current"],
                    interval_id=dict_intervals["current"].id,
                    apply=0,
                ).pack(),
            ),
        )

    return kb_builder.as_markup()
