from zoneinfo import ZoneInfo
from db.models import IntervalsORM, PagesORM
from keyboards.schedule.month_v2.classes_callback_data import MonthShudleCallbackData


from aiogram.types import InlineKeyboardButton


import datetime as dt


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


async def convert_datetime_to_time_str(
    defult_tz: ZoneInfo,
    time: dt.datetime,
) -> str:
    time_str: str = time.astimezone(defult_tz).strftime("%H:%M")
    return time_str


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
