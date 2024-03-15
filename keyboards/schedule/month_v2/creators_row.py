import datetime as dt
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardButton
from aiogram.utils.i18n import gettext as _

from db.models import IntervalsORM, PagesORM
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthScheduleCallbackData)


async def cr():
    pass


async def create_row_month_year(
        dict_datetimes: dict[str, dt.datetime],
        dict_pages: dict[str, PagesORM],
        dict_lineups: dict[str, int],
        dict_intervals: dict[str, IntervalsORM],
        current_page_interval_id: int,
        st_shifts: list[dict[str, str | int]] | None = None,
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": _("<"),
        },
        {
            "sequence_item": "current",
            "text": _('{month}').format(month=dict_datetimes["current"].strftime("%b")),
        },
        {
            "sequence_item": "current",
            "text": _('{year}').format(year=dict_datetimes["current"].year),
        },
        {
            "sequence_item": "after",
            "text": _(">"),
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_datetimes:
            day = 0
            month = dict_datetimes[button["sequence_item"]].month
            year = dict_datetimes[button["sequence_item"]].year
            page_id = dict_pages["current"].id
            lineup = dict_lineups["current"]
            interval_id = dict_intervals["current"].id
            page_interval_id = current_page_interval_id
            apply = 0
            button_ikb = InlineKeyboardButton(
                text=button["text"],
                callback_data=MonthScheduleCallbackData(
                    day=day,
                    month=month,
                    year=year,
                    page_id=page_id,
                    lineup=lineup,
                    interval_id=interval_id,
                    page_interval_id=page_interval_id,
                    apply=apply,
                ).pack(),
            )
            if st_shifts:
                if (
                        button["sequence_item"] != "before"
                        and button["sequence_item"] != "after"
                ):
                    buttons.append(button_ikb)
            else:
                buttons.append(button_ikb)
    return buttons


async def create_row_pages(
        dict_datetimes: dict[str, dt.datetime],
        dict_pages: dict[str, PagesORM],
        dict_lineups: dict[str, int],
        dict_intervals: dict[str, IntervalsORM],
        current_page_interval_id: int,
        st_shifts: list[dict[str, str | int]] | None = None,
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": _("<<<"),
        },
        {
            "sequence_item": "current",
            "text": _('{model_title}').format(model_title=dict_pages["current"].model.title),
        },
        {
            "sequence_item": "current",
            "text": _('{type_in_agency}').format(type_in_agency=dict_pages["current"].type_in_agency),
        },
        {
            "sequence_item": "after",
            "text": _(">>>"),
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_pages:
            day = 0
            month = dict_datetimes["current"].month
            year = dict_datetimes["current"].year
            page_id = dict_pages[button["sequence_item"]].id
            lineup = dict_lineups["current"]
            interval_id = dict_intervals["current"].id
            page_interval_id = current_page_interval_id
            apply = 0
            button_ikb = InlineKeyboardButton(
                text=button["text"],
                callback_data=MonthScheduleCallbackData(
                    day=day,
                    month=month,
                    year=year,
                    page_id=page_id,
                    lineup=lineup,
                    interval_id=interval_id,
                    page_interval_id=page_interval_id,
                    apply=apply,
                ).pack(),
            )
            if st_shifts:
                if (
                        button["sequence_item"] != "before"
                        and button["sequence_item"] != "after"
                ):
                    buttons.append(button_ikb)
            else:
                buttons.append(button_ikb)
    return buttons


async def convert_datetime_to_time_str(
        default_tz: ZoneInfo,
        time: dt.datetime,
) -> str:
    return _('{time_str}').format(time_str=time.astimezone(default_tz).strftime("%H:%M"))


async def create_row_intervals(
        dict_datetimes: dict[str, dt.datetime],
        dict_pages: dict[str, PagesORM],
        dict_lineups: dict[str, int],
        dict_intervals: dict[str, IntervalsORM],
        default_tz: ZoneInfo,
        current_page_interval_id: int,
        st_shifts: list[dict[str, str | int]] | None = None,
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": _("<<<"),
        },
        {
            "sequence_item": "current",
            "text": await convert_datetime_to_time_str(
                time=dict_intervals["current"].start_at,
                default_tz=default_tz,
            ),
        },
        {
            "sequence_item": "current",
            "text": await convert_datetime_to_time_str(
                time=dict_intervals["current"].end_at,
                default_tz=default_tz,
            ),
        },
        {
            "sequence_item": "after",
            "text": _(">>>"),
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_intervals:
            day = 0
            month = dict_datetimes["current"].month
            year = dict_datetimes["current"].year
            page_id = dict_pages["current"].id
            lineup = dict_lineups["current"]
            interval_id = dict_intervals[button["sequence_item"]].id
            page_interval_id = current_page_interval_id
            apply = 0
            button_ikb = InlineKeyboardButton(
                text=button["text"],
                callback_data=MonthScheduleCallbackData(
                    day=day,
                    month=month,
                    year=year,
                    page_id=page_id,
                    lineup=lineup,
                    interval_id=interval_id,
                    page_interval_id=page_interval_id,
                    apply=apply,
                ).pack(),
            )
            if st_shifts:
                if (
                        button["sequence_item"] != "before"
                        and button["sequence_item"] != "after"
                ):
                    buttons.append(button_ikb)
            else:
                buttons.append(button_ikb)
    return buttons


async def create_row_lineups(
        dict_datetimes: dict[str, dt.datetime],
        dict_pages: dict[str, PagesORM],
        dict_lineups: dict[str, int],
        dict_intervals: dict[str, IntervalsORM],
        current_page_interval_id: int,
        st_shifts: list[dict[str, str | int]] | None = None,
):
    buttons: list[InlineKeyboardButton] = []
    dict_for_ikb: list[dict[str, str]] = [
        {
            "sequence_item": "before",
            "text": _("<<<"),
        },
        {
            "sequence_item": "current",
            "text": _('{lineup}').format(lineup=dict_lineups["current"]),
        },
        {
            "sequence_item": "after",
            "text": _(">>>"),
        },
    ]
    for button in dict_for_ikb:
        if button["sequence_item"] in dict_lineups:
            day = 0
            month = dict_datetimes["current"].month
            year = dict_datetimes["current"].year
            page_id = dict_pages["current"].id
            lineup = dict_lineups[button["sequence_item"]]
            interval_id = dict_intervals["current"].id
            page_interval_id = current_page_interval_id
            apply = 0
            button_ikb = InlineKeyboardButton(
                text=button["text"],
                callback_data=MonthScheduleCallbackData(
                    day=day,
                    month=month,
                    year=year,
                    page_id=page_id,
                    lineup=lineup,
                    interval_id=interval_id,
                    page_interval_id=page_interval_id,
                    apply=apply,
                ).pack(),
            )
            if st_shifts:
                if (
                        button["sequence_item"] != "before"
                        and button["sequence_item"] != "after"
                ):
                    buttons.append(button_ikb)
            else:
                buttons.append(button_ikb)
    return buttons
