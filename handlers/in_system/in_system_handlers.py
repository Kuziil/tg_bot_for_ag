import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMFillReport
from callback_factories.back import BackCallbackData, ConfirmCallbackData
from db.models import PagesIntervalsORM, PagesORM, UsersORM
from db.requests.with_add import add_earning
from db.requests.with_page_interval import get_page_user_interval_by_page_interval_id
from db.requests.with_user import get_user_pages_shifts_earnings
from filters.filters import IsIntOrFloat
from handlers.in_system.schedules.month_v2_handlers import month_v2_router
from handlers.main_handlers import send_menu_and_clear_state
from keyboards.kb_single_line_horizontally import create_start_keyboard, create_confirm_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from keyboards.schedule.month_v2.classes_callback_data import MonthScheduleCallbackData
from lexicon.text_processor.processor import create_text_for_check_in_press, create_my_money, \
    text_for_process_day_press_in_report

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
    text: str = i18n["lexicon"]["schedule_type"]
    await callback.message.edit_text(
        text=text,
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
    text: str = i18n["lexicon"]["schedule"]
    await callback.message.edit_text(
        text=text,
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
    text: str = i18n['lexicon']['main_menu_junior']
    await callback.message.edit_text(text=text,
                                     reply_markup=create_menu_keyboard(
                                         "clock_out",
                                         "write_a_report",
                                         "schedule",
                                         "my_money",
                                         "model_statistics",
                                         "training_materials",
                                     ))
    start_at: datetime = datetime.now(tz=default_tz)
    texts_and_thread_ids: list[tuple[str, int]] = await create_text_for_check_in_press(session=session,
                                                                                       user_tg_id=callback.from_user.id,
                                                                                       start_at=start_at,
                                                                                       i18n=i18n)
    for text, thread_id in texts_and_thread_ids:
        await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=thread_id, text=text)


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
    text: str = i18n['lexicon']['main_menu_junior']
    await callback.message.edit_text(text=text,
                                     reply_markup=create_menu_keyboard(
                                         "check_in",
                                         "write_a_report",
                                         "schedule",
                                         "my_money",
                                         "model_statistics",
                                         "training_materials",
                                     ))
    end_at: datetime = datetime.now(tz=default_tz)
    texts_and_thread_ids = await create_text_for_check_in_press(session=session, user_tg_id=callback.from_user.id,
                                                                end_at=end_at, i18n=i18n)
    for text, thread_id in texts_and_thread_ids:
        await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=thread_id, text=text)


@in_system_router.callback_query(
    StateFilter(default_state),
    F.data == "write_a_report",
)
async def process_write_a_report_press(
        callback: CallbackQuery,
        i18n: dict[str, dict[str, str]],
        session: AsyncSession,
        default_tz: ZoneInfo,
        state: FSMContext
):
    text: str = i18n['lexicon']['select_shift_when_fill_report']
    await callback.message.edit_text(
        text=text,
        reply_markup=await create_month_schedule_v2(
            session=session,
            user_tg_id=callback.from_user.id,
            i18n=i18n,
            default_tz=default_tz,
        )
    )
    await state.set_state(FSMFillReport.page_interval_id)


@in_system_router.callback_query(
    StateFilter(FSMFillReport.page_interval_id),
    MonthScheduleCallbackData.filter(F.day > 0),
)
async def process_day_press_in_report(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        i18n: dict[str, dict[str, str]],
        state: FSMContext,
):
    text: str = await text_for_process_day_press_in_report(i18n=i18n, year=callback_data.day, month=callback_data.month,
                                                           day=callback_data.day)
    await callback.message.answer(text=text)
    await state.update_data(page_interval_id=callback_data.page_interval_id,
                            day=callback_data.day,
                            month=callback_data.month,
                            year=callback_data.year)
    await state.set_state(FSMFillReport.photos)


@in_system_router.callback_query(
    StateFilter(FSMFillReport.page_interval_id),
    MonthScheduleCallbackData.filter(),
)
async def process_not_day_press_in_report(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
        i18n: dict[str, dict[str, str]],
):
    text: str = i18n['lexicon']['select_shift_when_fill_report']
    markup = await create_month_schedule_v2(
        user_tg_id=callback.from_user.id,
        session=session,
        i18n=i18n,
        default_tz=default_tz,
        current_month=callback_data.month,
        current_year=callback_data.year,
        current_day=callback_data.day,
        current_page_id=callback_data.page_id,
        current_interval_id=callback_data.interval_id,
        current_lineup=callback_data.lineup,
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=markup
    )
    await callback.answer()


@in_system_router.message(
    StateFilter(FSMFillReport.photos),
    F.photo
)
async def process_send_photos(
        message: Message,
        state: FSMContext,
):
    st = await state.get_data()
    try:
        st_photos = st['photos']
    except KeyError:
        st_photos = []
    photos = message.photo[-1]
    st_photos.append(photos.file_id)
    await state.update_data(photos=st_photos)


@in_system_router.message(
    StateFilter(FSMFillReport.photos),
    IsIntOrFloat()
)
async def process_send_text(
        message: Message,
        state: FSMContext,
        i18n: dict[str, dict[str, str]],
        dirty: int | float,
):
    await state.update_data(dirty=dirty)
    st = await state.get_data()
    media_group = MediaGroupBuilder(caption=str(st['dirty']))
    for photo_id in st['photos']:
        media_group.add_photo(media=photo_id)
    await message.answer_media_group(media=media_group.build())

    text: str = i18n['lexicon']['is_that_correct']
    await message.answer(text=text,
                         reply_markup=create_start_keyboard(
                             'back_from_process_send_text',
                             'all_correct_in_report'
                         ))
    await state.set_state(FSMFillReport.dirty)


@in_system_router.callback_query(
    StateFilter(FSMFillReport.dirty),
    F.data == 'all_correct_in_report'
)
async def process_all_correct_in_report(
        callback: CallbackQuery,
        session: AsyncSession,
        state: FSMContext,
        i18n: dict[str, dict[str, str]],
):
    st = await state.get_data()
    page_interval: PagesIntervalsORM = await get_page_user_interval_by_page_interval_id(
        session=session, user_tg_id=callback.from_user.id, page_interval_id=st['page_interval_id']
    )
    page: PagesORM = page_interval.page
    thread_id: int = page.report_thread_id
    text_1: str = f"{i18n['lexicon']['send_report_to_topik']} {st['dirty']}"
    media_group = MediaGroupBuilder(caption=text_1)
    for photo_id in st['photos']:
        media_group.add_photo(media=photo_id)
    messages = await callback.bot.send_media_group(chat_id=-1002098324148, message_thread_id=thread_id,
                                                   media=media_group.build())
    message_to_reply = messages[0]
    message_to_reply_id = message_to_reply.message_id
    text_2: str = i18n['lexicon']['report_is_right_or_not']
    await callback.bot.send_message(text=text_2, chat_id=-1002098324148, message_thread_id=thread_id,
                                    reply_to_message_id=message_to_reply_id,
                                    reply_markup=await create_confirm_keyboard(
                                        day=st["day"],
                                        month=st["month"],
                                        year=st["year"],
                                        page_interval_id=st["page_interval_id"],
                                        dirty=st["dirty"]
                                    ))
    text_3: str = i18n['lexicon']['main_menu_junior']
    await send_menu_and_clear_state(callback=callback, text=text_3, state=state)


@in_system_router.callback_query(
    ConfirmCallbackData.filter()
)
async def process_confirm(
        callback: CallbackQuery,
        callback_data: ConfirmCallbackData,
        session: AsyncSession,
        i18n: dict[str, dict[str, str]],
):
    await add_earning(
        session=session,
        page_interval_id=callback_data.page_interval_id,
        day=callback_data.day,
        month=callback_data.month,
        year=callback_data.year,
        dirty=callback_data.dirty
    )
    text: str = i18n['lexicon']['report_is_right']
    await callback.message.edit_text(text=text)


@in_system_router.callback_query(
    F.data == "my_money"
)
async def process_press_my_money(
        callback: CallbackQuery,
        session: AsyncSession,
        i18n: dict[str, dict[str, str]],
):
    user: UsersORM = await get_user_pages_shifts_earnings(session=session, user_tg_id=callback.from_user.id)
    text: str = await create_my_money(user=user, i18n=i18n)
    await callback.message.edit_text(text=text)
