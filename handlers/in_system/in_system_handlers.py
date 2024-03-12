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
from callback_factories.back import BackCallbackData
from db.models import PagesIntervalsORM, PagesORM
from db.requests.with_page_interval import get_page_user_interval_by_page_interval_id
from filters.filters import IsIntOrFloat
from handlers.in_system.schedules.month_v2_handlers import month_v2_router
from keyboards.kb_single_line_horizontally import create_start_keyboard
from keyboards.kb_single_line_vertically import create_menu_keyboard
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from keyboards.schedule.month_v2.classes_callback_data import MonthScheduleCallbackData
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
    text_and_thread_id = await create_text_for_check_in_press(session=session, user_tg_id=callback.from_user.id,
                                                              start_at=start_at)
    for text, thread_id in text_and_thread_id:
        await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=thread_id, text=text)
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
    text_and_thread_id = await create_text_for_check_in_press(session=session, user_tg_id=callback.from_user.id,
                                                              end_at=end_at)
    for text, thread_id in text_and_thread_id:
        await callback.bot.send_message(chat_id=-1002078072009, message_thread_id=thread_id, text=text)
    await callback.message.edit_text(text="1",
                                     reply_markup=create_menu_keyboard(
                                         "check_in",
                                         "write_a_report",
                                         "schedule",
                                         "my_money",
                                         "model_statistics",
                                         "training_materials",
                                     ), )


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
    await callback.message.edit_text(
        text="Пожалуйста выберите страницу и дату",
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
    await callback.message.answer(
        text=f"Отправьте фото для\n"
             f"{callback_data.year}.{callback_data.month}.{callback_data.day}",
    )
    await state.update_data(page_interval_id=callback_data.page_interval_id)
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
    await callback.message.edit_text(
        text="22",
        reply_markup=await create_month_schedule_v2(
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
        ),
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
        dirty: int | float,
):
    await state.update_data(dirty=dirty)
    st = await state.get_data()
    media_group = MediaGroupBuilder(caption=str(st['dirty']))
    for photo_id in st['photos']:
        media_group.add_photo(media=photo_id)
    await message.answer_media_group(media=media_group.build())
    await message.answer(text="Данные верны?",
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
    media_group = MediaGroupBuilder(caption=str(st['dirty']))
    for photo_id in st['photos']:
        media_group.add_photo(media=photo_id)
    await callback.bot.send_media_group(chat_id=-1002098324148, message_thread_id=thread_id, media=media_group.build())
    await state.clear()
    await callback.message.edit_text(
        text=i18n['lexicon']['main_menu_junior'],
        reply_markup=create_menu_keyboard(
            "check_in",
            "clock_out",
            "write_a_report",
            "schedule",
            "my_money",
            "model_statistics",
            "training_materials",
        ),
    )
    await callback.answer()
