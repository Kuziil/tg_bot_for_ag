from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM
from db.requests.with_shift import update_starts_at_in_shifts


async def create_text_for_check_in_press(
        session: AsyncSession,
        user_tg_id: int,
        start_at: datetime,
) -> str:
    shifts: list[ShiftsORM] = await update_starts_at_in_shifts(session=session, user_tg_id=user_tg_id,
                                                               start_at=start_at)
    user: UsersORM | None = None
    text: str | None = None
    formatted_date = start_at.strftime('%Y-%m-%d %H:%M %Z')
    for shift in shifts:
        page_interval: PagesIntervalsORM = shift.page_interval
        page: PagesORM = page_interval.page
        if user is None:
            user: UsersORM = page_interval.user
            username: str = user.username
            emoji: str = user.emoji
            text: str = (f'{emoji}{username}\n'
                         f'Начал смену в {formatted_date}\n'
                         f'на страницах:\n')
        page_title: str = page.title
        text += page_title
    return text
