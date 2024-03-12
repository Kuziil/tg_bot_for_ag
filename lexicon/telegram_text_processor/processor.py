from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM
from db.requests.with_shift import update_starts_at_in_shifts


async def create_text_for_check_in_press(
        session: AsyncSession,
        user_tg_id: int,
        start_at: datetime | None = None,
        end_at: datetime | None = None
) -> str:
    if start_at is not None:
        formatted_date = start_at.strftime('%Y-%m-%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   start_at=start_at)
        start_or_end = "Начал"
    else:
        formatted_date = end_at.strftime('%Y-%m-%d %H:%M %Z')
        shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                                   end_at=end_at)
        start_or_end = "Закончил"
    user: UsersORM | None = None
    text: str | None = None
    for shift in shifts:
        page_interval: PagesIntervalsORM = shift.page_interval
        page: PagesORM = page_interval.page
        if user is None:
            user: UsersORM = page_interval.user
            username: str = user.username
            emoji: str = user.emoji
            text: str = (f'{emoji}{username}\n'
                         f'{start_or_end} смену в {formatted_date}\n'
                         f'на страницах:\n')
        page_title: str = page.title
        text += page_title
    return text
