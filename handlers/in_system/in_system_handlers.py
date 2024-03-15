import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import gettext as _

from FSMs.FSMs import FSMFillReport
from db.models import UsersORM
from db.requests.with_user import get_user_pages_shifts_earnings
from handlers.in_system.report.report_handlers import report_router
from handlers.in_system.schedules.month_v2_handlers import month_v2_router
from keyboards.kb_single_line_vertically import create_menu_keyboard
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from lexicon.text_processor.processor import create_my_money, create_text_for_check_in_press

in_system_router = Router()

in_system_router.include_router(month_v2_router)
in_system_router.include_router(report_router)

logger = logging.getLogger(__name__)


@in_system_router.callback_query(
    F.data == "schedule",
    StateFilter(default_state),
)
async def process_month_schedule_press(
        callback: CallbackQuery,
        session: AsyncSession,
        default_tz: ZoneInfo,
):
    await callback.message.edit_text(
        text=_('Выберете интересующую дату'),
        reply_markup=await create_month_schedule_v2(
            session=session,
            user_tg_id=callback.from_user.id,
            default_tz=default_tz,
        ),
    )
    await callback.answer()


@in_system_router.callback_query(
    StateFilter(default_state),
    F.data == "check_in",
)
async def process_check_in_press(
        callback: CallbackQuery,
        session: AsyncSession,
        default_tz: ZoneInfo,
):
    await callback.message.edit_text(text=_('Выберите интересующую опцию'),
                                     reply_markup=create_menu_keyboard(
                                         "clock_out",
                                     ))
    start_at: datetime = datetime.now(tz=default_tz)
    texts_and_thread_ids: list[tuple[str, int]] = await create_text_for_check_in_press(session=session,
                                                                                       user_tg_id=callback.from_user.id,
                                                                                       start_at=start_at)
    for text, thread_id in texts_and_thread_ids:
        await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=thread_id, text=text)


@in_system_router.callback_query(
    StateFilter(default_state),
    F.data == "clock_out",
)
async def process_clock_out_press(
        callback: CallbackQuery,
        session: AsyncSession,
        default_tz: ZoneInfo,
):
    await callback.message.edit_text(text=_('выберите интересующую вас опцию'),
                                     reply_markup=create_menu_keyboard(
                                         "check_in",
                                         "write_a_report",
                                         "schedule",
                                         "my_money",
                                     ))
    end_at: datetime = datetime.now(tz=default_tz)
    texts_and_thread_ids = await create_text_for_check_in_press(session=session, user_tg_id=callback.from_user.id,
                                                                end_at=end_at)
    for text, thread_id in texts_and_thread_ids:
        await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=thread_id, text=text)


@in_system_router.callback_query(
    StateFilter(default_state),
    F.data == "write_a_report",
)
async def process_write_a_report_press(
        callback: CallbackQuery,
        session: AsyncSession,
        default_tz: ZoneInfo,
        state: FSMContext
):
    await callback.message.edit_text(
        text=_('Пожалуйста выберите страницу и дату смены'),
        reply_markup=await create_month_schedule_v2(
            session=session,
            user_tg_id=callback.from_user.id,
            default_tz=default_tz,
        )
    )
    await state.set_state(FSMFillReport.page_interval_id)


@in_system_router.callback_query(
    F.data == "my_money"
)
async def process_press_my_money(
        callback: CallbackQuery,
        session: AsyncSession,
):
    user: UsersORM = await get_user_pages_shifts_earnings(session=session, user_tg_id=callback.from_user.id)
    text: str = await create_my_money(user=user)
    await callback.message.edit_text(text=text)
