from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from FSMs.FSMs import FSMFillReport
from callback_factories.back import ConfirmCallbackData
from db.models import PagesIntervalsORM, PagesORM
from db.requests.with_add import add_earning
from db.requests.with_page_interval import get_page_user_interval_by_page_interval_id
from filters.filters import IsIntOrFloat
from handlers.DRY import send_menu_and_clear_state
from keyboards.kb_single_line_horizontally import create_start_keyboard, create_confirm_keyboard
from keyboards.schedule.month_v2.builder import create_month_schedule_v2
from keyboards.schedule.month_v2.classes_callback_data import MonthScheduleCallbackData

report_router = Router()


@report_router.callback_query(
    StateFilter(FSMFillReport.page_interval_id),
    MonthScheduleCallbackData.filter(F.day > 0),
)
async def process_day_press_in_report(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        state: FSMContext,
):
    await callback.message.answer(
        text=_('Отправьте фото для\nсмены прошедшей {day}.{month}.{year}').format(day=callback_data.day,
                                                                                  month=callback_data.month,
                                                                                  year=callback_data.year))
    await state.update_data(page_interval_id=callback_data.page_interval_id,
                            day=callback_data.day,
                            month=callback_data.month,
                            year=callback_data.year)
    await state.set_state(FSMFillReport.photos)


@report_router.callback_query(
    StateFilter(FSMFillReport.page_interval_id),
    MonthScheduleCallbackData.filter(),
)
async def process_not_day_press_in_report(
        callback: CallbackQuery,
        callback_data: MonthScheduleCallbackData,
        session: AsyncSession,
        default_tz: ZoneInfo,
):
    await callback.message.edit_text(
        text=_('Пожалуйста выберите страницу и дату смены'),
        reply_markup=await create_month_schedule_v2(
            user_tg_id=callback.from_user.id,
            session=session,
            default_tz=default_tz,
            current_month=callback_data.month,
            current_year=callback_data.year,
            current_day=callback_data.day,
            current_page_id=callback_data.page_id,
            current_interval_id=callback_data.interval_id,
            current_lineup=callback_data.lineup,
        )
    )
    await callback.answer()


@report_router.message(
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


@report_router.message(
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
    media_group = MediaGroupBuilder(caption=_('{dirty}$').format(dirty=st['dirty']))
    for photo_id in st['photos']:
        media_group.add_photo(media=photo_id)

    await message.answer_media_group(media=media_group.build())

    await message.answer(text=_('Проверьте, верны ли данные перед отправкой'),
                         reply_markup=create_start_keyboard(
                             'back_from_process_send_text',
                             'all_correct_in_report'
                         ))

    await state.set_state(FSMFillReport.dirty)


@report_router.callback_query(
    StateFilter(FSMFillReport.dirty),
    F.data == 'all_correct_in_report'
)
async def process_all_correct_in_report(
        callback: CallbackQuery,
        session: AsyncSession,
        state: FSMContext,
):
    st = await state.get_data()
    page_interval: PagesIntervalsORM = await get_page_user_interval_by_page_interval_id(
        session=session, user_tg_id=callback.from_user.id, page_interval_id=st['page_interval_id']
    )
    page: PagesORM = page_interval.page
    thread_id: int = page.report_thread_id
    media_group = MediaGroupBuilder(caption=_('Заработано - {dirty}').format(dirty=st['dirty']))
    for photo_id in st['photos']:
        media_group.add_photo(media=photo_id)
    messages = await callback.bot.send_media_group(chat_id=-1002098324148, message_thread_id=thread_id,
                                                   media=media_group.build())
    message_to_reply = messages[0]
    message_to_reply_id = message_to_reply.message_id
    await callback.bot.send_message(text=_('Проверьте отчет, и если все верно, подтвердите'),
                                    chat_id=-1002098324148,
                                    message_thread_id=thread_id,
                                    reply_to_message_id=message_to_reply_id,
                                    reply_markup=await create_confirm_keyboard(
                                        day=st["day"],
                                        month=st["month"],
                                        year=st["year"],
                                        page_interval_id=st["page_interval_id"],
                                        dirty=st["dirty"]
                                    ))
    await send_menu_and_clear_state(callback=callback, text=_('Отчет успешно отправлен'), state=state)


@report_router.callback_query(
    ConfirmCallbackData.filter()
)
async def process_confirm(
        callback: CallbackQuery,
        callback_data: ConfirmCallbackData,
        session: AsyncSession,
):
    await add_earning(
        session=session,
        page_interval_id=callback_data.page_interval_id,
        day=callback_data.day,
        month=callback_data.month,
        year=callback_data.year,
        dirty=callback_data.dirty
    )
    await callback.message.edit_text(text=_('Отчет подтвержден'))
