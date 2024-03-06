from zoneinfo import ZoneInfo
from db.models import IntervalsORM, PagesORM
from keyboards.schedule.month_v2.classes_callback_data import (
    MonthScheduleCallbackData)


from aiogram.types import InlineKeyboardButton


import datetime as dt


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
            "text": "<",
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
            "text": ">",
        },
    ]
    for button in dict_for_ikb:
        if st_shifts:
            if (
                button["sequence_item"] != "before"
                and button["sequence_item"] != "after"
                and button["sequence_item"] in dict_datetimes
            ):
                month = dict_datetimes[button["sequence_item"]].month
                year = dict_datetimes[button["sequence_item"]].year
                page_id = dict_pages["current"].id
                lineup = dict_lineups["current"]
                interval_id = dict_intervals["current"].id
                page_interval_id = current_page_interval_id
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=month,
                            year=year,
                            page_id=page_id,
                            lineup=lineup,
                            interval_id=interval_id,
                            page_interval_id=page_interval_id,
                            apply=0,
                        ).pack(),
                    )
                )
        else:
            if button["sequence_item"] in dict_datetimes:
                month = dict_datetimes[button["sequence_item"]].month
                year = dict_datetimes[button["sequence_item"]].year
                page_id = dict_pages["current"].id
                lineup = dict_lineups["current"]
                interval_id = dict_intervals["current"].id
                page_interval_id = current_page_interval_id
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=month,
                            year=year,
                            page_id=page_id,
                            lineup=lineup,
                            interval_id=interval_id,
                            page_interval_id=page_interval_id,
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
    current_page_interval_id: int,
    st_shifts: list[dict[str, str | int]] | None = None,
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
        if st_shifts:
            if (
                button["sequence_item"] != "before"
                and button["sequence_item"] != "after"
                and button["sequence_item"] in dict_pages
            ):
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=dict_datetimes["current"].month,
                            year=dict_datetimes["current"].year,
                            page_id=dict_pages[button["sequence_item"]].id,
                            lineup=dict_lineups["current"],
                            interval_id=dict_intervals["current"].id,
                            page_interval_id=current_page_interval_id,
                            apply=0,
                        ).pack(),
                    )
                )
        else:
            if button["sequence_item"] in dict_pages:
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=dict_datetimes["current"].month,
                            year=dict_datetimes["current"].year,
                            page_id=dict_pages[button["sequence_item"]].id,
                            lineup=dict_lineups["current"],
                            interval_id=dict_intervals["current"].id,
                            page_interval_id=current_page_interval_id,
                            apply=0,
                        ).pack(),
                    )
                )
    return buttons


async def convert_datetime_to_time_str(
    default_tz: ZoneInfo,
    time: dt.datetime,
) -> str:
    time_str: str = time.astimezone(default_tz).strftime("%H:%M")
    return time_str


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
            "text": "<<<",
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
            "text": ">>>",
        },
    ]
    for button in dict_for_ikb:
        if st_shifts:
            if (
                button["sequence_item"] != "before"
                and button["sequence_item"] != "after"
                and button["sequence_item"] in dict_intervals
            ):
                month = dict_datetimes["current"].month
                year = dict_datetimes["current"].year
                page_id = dict_pages["current"].id
                lineup = dict_lineups["current"]
                interval_id = dict_intervals[button["sequence_item"]].id
                page_interval_id = current_page_interval_id
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=month,
                            year=year,
                            page_id=page_id,
                            lineup=lineup,
                            interval_id=interval_id,
                            page_interval_id=page_interval_id,
                            apply=0,
                        ).pack(),
                    )
                )
        else:
            if button["sequence_item"] in dict_intervals:
                month = dict_datetimes["current"].month
                year = dict_datetimes["current"].year
                page_id = dict_pages["current"].id
                lineup = dict_lineups["current"]
                interval_id = dict_intervals[button["sequence_item"]].id
                page_interval_id = current_page_interval_id
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=month,
                            year=year,
                            page_id=page_id,
                            lineup=lineup,
                            interval_id=interval_id,
                            page_interval_id=page_interval_id,
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
    current_page_interval_id: int,
    st_shifts: list[dict[str, str | int]] | None = None,
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
        if st_shifts:
            if (
                button["sequence_item"] != "before"
                and button["sequence_item"] != "after"
                and button["sequence_item"] in dict_lineups
            ):
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=dict_datetimes["current"].month,
                            year=dict_datetimes["current"].year,
                            page_id=dict_pages["current"].id,
                            lineup=dict_lineups[button["sequence_item"]],
                            interval_id=dict_intervals["current"].id,
                            page_interval_id=current_page_interval_id,
                            apply=0,
                        ).pack(),
                    )
                )
        else:
            if button["sequence_item"] in dict_lineups:
                buttons.append(
                    InlineKeyboardButton(
                        text=button["text"],
                        callback_data=MonthScheduleCallbackData(
                            day=0,
                            month=dict_datetimes["current"].month,
                            year=dict_datetimes["current"].year,
                            page_id=dict_pages["current"].id,
                            lineup=dict_lineups[button["sequence_item"]],
                            interval_id=dict_intervals["current"].id,
                            page_interval_id=current_page_interval_id,
                            apply=0,
                        ).pack(),
                    )
                )
    return buttons
