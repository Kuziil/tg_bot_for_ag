import logging
from datetime import datetime
from typing import TYPE_CHECKING

from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM, EarningsORM
from db.requests.with_shift import update_starts_at_in_shifts


logger = logging.getLogger(__name__)


async def create_text_for_check_in_press(
        session: AsyncSession,
        user_tg_id: int,
        i18n: TranslatorRunner,
        start_at: datetime | None = None,
        end_at: datetime | None = None,

) -> list[tuple[str, int]]:
    text_and_thread_id: list[tuple[str, int]] = []
    if start_at is not None:
        formatted_date = start_at.strftime('%Y.%m.%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   start_at=start_at)
        start_or_end = True
    else:
        formatted_date = end_at.strftime('%Y.%m.%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   end_at=end_at)
        start_or_end = False
    for shift in shifts:
        page_interval: PagesIntervalsORM = shift.page_interval
        page: PagesORM = page_interval.page
        user: UsersORM = page_interval.user
        thread_id: int = page.reshift_thread_id
        if start_or_end is True:
            text: str = i18n.text.in_agency.check_in_or_clock_out(userEmoji=user.emoji, userTgId=user_tg_id,
                                                                  checkInOrClockOut="check_in",
                                                                  userName=user.username, formattedDate=formatted_date)
        else:
            text: str = i18n.text.in_agency.check_in_or_clock_out(userEmoji=user.emoji, userTgId=user_tg_id,
                                                                  checkInOrClockOut="clock_out",
                                                                  userName=user.username, formattedDate=formatted_date)
        text_and_thread_id.append((text, thread_id))
    return text_and_thread_id


async def create_my_money(user: UsersORM, i18n: TranslatorRunner) -> str:
    pages_intervals: list[PagesIntervalsORM] = user.pages_intervals
    text = i18n.text.in_agency.my_money.head()
    for page_interval in pages_intervals:
        page: PagesORM = page_interval.page
        total_dirty_earnings: int = 0
        for shift in page_interval.shifts:  # type: ShiftsORM
            for earning in shift.earnings:  # type: EarningsORM
                total_dirty_earnings += int(earning.dirty)
        text += i18n.text.in_agency.my_money.body(pageTitle=page.title, totalDirtyEarnings=total_dirty_earnings)
    return text
