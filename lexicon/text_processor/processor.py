import logging
from datetime import datetime

from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ShiftsORM, PagesIntervalsORM, UsersORM, PagesORM, EarningsORM
from db.requests.with_shift import update_starts_at_in_shifts

logger = logging.getLogger(__name__)


async def create_text_for_check_in_press(
        session: AsyncSession,
        user_tg_id: int,
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
            text: str = _('{emoji}<a href="tg://user?id={user_tg_id}">{username}</a>\n'
                          '🟩 Начал смену\n'
                          '<b>{formatted_date}</b>\n').format(emoji=user.emoji, user_tg_id=user_tg_id,
                                                              username=user.username, formatted_date=formatted_date)
        else:
            text: str = _('{emoji}<a href="tg://user?id={user_tg_id}">{username}</a>\n'
                          '🟥 Закончил\n'
                          '<b>{formatted_date}</b>\n').format(emoji=user.emoji, user_tg_id=user_tg_id,
                                                              username=user.username, formatted_date=formatted_date)
        text_and_thread_id.append((text, thread_id))
    return text_and_thread_id


async def create_my_money(user: UsersORM) -> str:
    pages_intervals: list[PagesIntervalsORM] = user.pages_intervals
    text = _('Ожидает оплаты \n')
    for page_interval in pages_intervals:
        page: PagesORM = page_interval.page
        total_dirty_earnings: int = 0
        for shift in page_interval.shifts:  # type: ShiftsORM
            for earning in shift.earnings:  # type: EarningsORM
                total_dirty_earnings += earning.dirty
        text += _('{page_title}: {total_dirty_earnings}$\n').format(page_title=page.title,
                                                                    total_dirty_earnings=total_dirty_earnings)
    return text


async def text_for_process_emoji_sent(
        username: str,
        emoji: str,
):
    text: str = _("Регистрация успешно выполнена\n\n"
                  "{username}{emoji}\n\n"
                  "Выберите интересующую вас опцию").format(username=username,
                                                            emoji=emoji)
    return text


async def text_for_user_in_menu(
        role_dict: dict[str, int | str | list[int] | list[str]],
) -> str:
    role: str | None = None
    match role_dict["role_id"]:
        case 1:
            role = _("оператор")
        case 2:
            role = _("старший оператор")
        case 3:
            role = _("руководитель")
    text: str = _("Приветствую, {emoji}{role} {username}, "
                  "выберите интересующую опцию").format(emoji=role_dict["emoji"],
                                                        role=role,
                                                        username=role_dict["username"])
    return text
