import matplotlib.pyplot as plt
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from fluentogram import TranslatorRunner
from sqlalchemy.ext.asyncio import AsyncSession

from callback_factories.back import PagesCallbackData
from db.requests.with_page import get_all_pages
from keyboards.kb_single_line_vertically import create_kb_pages_and_back_forward

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
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']
    customer_calls = [20, 30, 25, 35, 40]

    with plt.style.context('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle'):
        plt.plot(days, customer_calls, marker='o')
        plt.title('Коли')
        plt.xlabel('День недели')
        plt.ylabel('Количество обращений')
        plt.grid(True)
        plt.savefig('customer_calls.png')
    await callback.message.answer_photo(photo=FSInputFile("customer_calls.png"))
