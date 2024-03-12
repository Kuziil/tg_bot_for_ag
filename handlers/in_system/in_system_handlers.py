import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.filters import or_f
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from callback_factories.back import BackCallbackData
from handlers.in_system.schedules.month_v2_handlers import month_v2_router
from keyboards.kb_single_line_vertically import create_menu_keyboard
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from lexicon.telegram_text_processor.processor import create_text_for_check_in_press

in_system_router = Router()

in_system_router.include_router(month_v2_router)

logger = logging.getLogger(__name__)


@in_system_router.callback_query(
    StateFilter(default_state),
    or_f(
        F.data == "schedule",
        BackCallbackData.filter(F.handler == "process_schedule_press"),
    ),
)
async def process_schedule_press(
        callback: CallbackQuery,
        i18n: dict[str, dict[str, str]],
):
    """Данный хэндлер отрабатывает на нажатие кнопки расписание ->
    выдает инлайн клавиатуру с типами расписания

    Args:
        i18n:
        callback (CallbackQuery): _description_
    """
    await callback.message.edit_text(
        text=i18n["lexicon"]["schedule_type"],
        reply_markup=create_menu_keyboard(
            "month_schedule",
            "week_schedule",
        ),
    )
    await callback.answer()


@in_system_router.callback_query(
    F.data == "week_schedule",
    StateFilter(default_state),
)
async def process_month_schedule_press(
        callback: CallbackQuery,
        session: AsyncSession,
        i18n: dict[str, dict[str, str]],
        default_tz: ZoneInfo,
):
    await callback.message.edit_text(
        text=i18n["lexicon"]["week_schedule"],
        reply_markup=await create_month_schedule_v2(
            session=session,
            user_tg_id=callback.from_user.id,
            i18n=i18n,
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
        i18n: dict[str, dict[str, str]],
        session: AsyncSession,
        default_tz: ZoneInfo,
):
    start_at: datetime = datetime.now(tz=default_tz)
    text = await create_text_for_check_in_press(session=session, user_tg_id=callback.from_user.id,
                                                start_at=start_at)
    await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=3, text=text)
    await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=5, text=text)
    await callback.message.edit_text(text='1',
                                     reply_markup=create_menu_keyboard(
                                         "clock_out",
                                         "write_a_report",
                                         "schedule",
                                         "my_money",
                                         "model_statistics",
                                         "training_materials",
                                     ), )


@in_system_router.callback_query(
    StateFilter(default_state),
    F.data == "clock_out",
)
async def process_clock_out_press(
        callback: CallbackQuery,
        i18n: dict[str, dict[str, str]],
        session: AsyncSession,
        default_tz: ZoneInfo,
):
    end_at: datetime = datetime.now(tz=default_tz)
    text = await create_text_for_check_in_press(session=session, user_tg_id=callback.from_user.id,
                                                end_at=end_at)
    await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=3, text=text)
    await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=5, text=text)
    await callback.message.edit_text(text="1",
                                     reply_markup=create_menu_keyboard(
                                         "check_in",
                                         "write_a_report",
                                         "schedule",
                                         "my_money",
                                         "model_statistics",
                                         "training_materials",
                                     ), )
