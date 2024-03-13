import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM, EarningsORM
from db.requests.with_shift import update_starts_at_in_shifts

logger = logging.getLogger(__name__)


async def create_text_for_check_in_press(
        session: AsyncSession,
        user_tg_id: int,
        i18n: dict[str, dict[str, str]],
        start_at: datetime | None = None,
        end_at: datetime | None = None,

) -> list[tuple[str, int]]:
    text_and_thread_id: list[tuple[str, int]] = []
    if start_at is not None:
        formatted_date = start_at.strftime('%Y.%m.%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   start_at=start_at)
        start_or_end = i18n['lexicon']['start']
    else:
        formatted_date = end_at.strftime('%Y.%m.%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   end_at=end_at)
        start_or_end = i18n['lexicon']['end']
    for shift in shifts:
        page_interval: PagesIntervalsORM = shift.page_interval
        page: PagesORM = page_interval.page
        user: UsersORM = page_interval.user
        username: str = user.username
        emoji: str = user.emoji
        thread_id: int = page.reshift_thread_id
        logger.debug(user_tg_id)
        text: str = (f'{emoji}<a href="tg://user?id={user_tg_id}">{username}</a>\n'
                     f'{start_or_end} смену\n'
                     f'<b>{formatted_date}</b>\n')
        text_and_thread_id.append((text, thread_id))
    return text_and_thread_id


async def create_my_money(user: UsersORM, i18n: dict[str, dict[str, str]]) -> str:
    pages_intervals: list[PagesIntervalsORM] = user.pages_intervals
    text = i18n['lexicon']['waiting_for_payment']
    for page_interval in pages_intervals:
        page: PagesORM = page_interval.page
        page_title: str = page.title
        total_dirty_earnings: int = 0
        for shift in page_interval.shifts:  # type: ShiftsORM
            for earning in shift.earnings:  # type: EarningsORM
                total_dirty_earnings += earning.dirty
        text += f'{page_title}: {total_dirty_earnings}$\n'
    return text


async def text_for_process_emoji_sent(
        username: str,
        emoji: str,
        i18n: dict[str, dict[str, str]],
):
    text_1: str = i18n['lexicon']["registration_done"]
    text_2: str = i18n['lexicon']["main_menu_junior"]
    text: str = (f"{text_1} {username}{emoji}\n\n"
                 f"{text_2}")
    return text


async def text_for_process_day_press_in_report(
        i18n: dict[str, dict[str, str]],
        year: int,
        month: int,
        day: int
):
    text_1: str = i18n['lexicon']['send_photo']
    text = (f'{text_1}'
            f'{day}.{month}.{year}')
    return text
