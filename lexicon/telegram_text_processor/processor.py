import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM
from db.requests.with_shift import update_starts_at_in_shifts

logger = logging.getLogger(__name__)


async def create_text_for_check_in_press(
        session: AsyncSession,
        user_tg_id: int,
        start_at: datetime | None = None,
        end_at: datetime | None = None
) -> list[tuple[str, int]]:
    text_and_thread_id: list[tuple[str, int]] = []
    if start_at is not None:
        formatted_date = start_at.strftime('%Y-%m-%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   start_at=start_at)
        start_or_end = "🟩 Начал"
    else:
        formatted_date = end_at.strftime('%Y-%m-%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   end_at=end_at)
        start_or_end = "🟥 Закончил"
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
