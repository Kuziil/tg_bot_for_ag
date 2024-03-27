import io

import matplotlib.pyplot as plt
from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from callback_factories.back import PagesCallbackData
from db.requests.with_page import get_all_pages
from keyboards.kb_single_line_vertically import create_kb_pages_and_back_forward
from utils.graphics import create_graphics_for_pages

statistic_router = Router()


@statistic_router.callback_query(
    F.data == "statistics_of_all_pages"
)
async def process_statistics_of_all_pages(
        callback: CallbackQuery,
        session: AsyncSession,
        agency_id: int,
        i18n: TranslatorRunner,
):
    await callback.message.edit_text(text=i18n.text.statistic.select.page(),
                                     reply_markup=create_kb_pages_and_back_forward(
                                         i18n=i18n,
                                         pages=await get_all_pages(
                                             session=session, agency_id=agency_id, user_tg_id=callback.from_user.id
                                         ),
                                         user_tg_id=callback.from_user.id))


@statistic_router.callback_query(
    PagesCallbackData.filter()
)
async def process_page_in_statistic_press(
        callback: CallbackQuery,
        callback_data: PagesCallbackData,
        i18n: TranslatorRunner,
):
    buffer = create_graphics_for_pages()
    await callback.message.answer_photo(photo=BufferedInputFile(buffer.read(), filename='plot.png'))
