import logging
import datetime as dt
from zoneinfo import ZoneInfo

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

# from lexicon.lexicon_ru import LEXICON_RU

from db.requests.with_add import add_model, add_page, add_page_interval, add_interval
from db.requests.with_page import get_pages_with_inter_users_tgs_by_user_tg_id, test_123
from db.requests.with_interval import get_interval_by_id
from db.requests.with_user import get_user_and_availible_pages_intervals_by_tg_id
from db.models import PagesIntervalsORM, TgsORM
from keyboards.schedule.month_v2.bilder import create_month_shudle_v2

router = Router()

logger = logging.getLogger(__name__)


# # test shifts


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
#     defult_tz: ZoneInfo,
#     i18n: dict,
# ):
#     pages_intervals = await test_123(
#         session=session,
#     )
#     for page_interval in pages_intervals:
#         logger.debug(page_interval)
#         for shift in page_interval.shifts:
#             logger.debug(shift)
#     await message.answer(text="1")


# test create_mounth_shudle_v2


@router.message(StateFilter(default_state))
async def send_echo(
    message: Message,
    session: AsyncSession,
    defult_tz: ZoneInfo,
    i18n: dict,
):
    await message.answer(
        text="1",
        reply_markup=await create_month_shudle_v2(
            session=session,
            user_tg_id=message.from_user.id,
            defult_tz=defult_tz,
            i18n=i18n,
        ),
    )


# # get_interval_by_id


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
# ):
#     interval = await get_interval_by_id(
#         session=session,
#         interval_id=message.text,
#     )
#     await message.answer(
#         text=f"{interval.id} - {interval.start_at} - {interval.end_at}",
#     )


# add_interval


@router.message(StateFilter(default_state))
async def send_echo(
    message: Message,
    session: AsyncSession,
    defult_tz: ZoneInfo,
):
    interval = message.text.split("-")
    start_at = dt.datetime.strptime(interval[0], "%H:%M").time()
    end_at = dt.datetime.strptime(interval[1], "%H:%M").time()
    await add_interval(
        session=session,
        defult_tz=defult_tz,
        start_at=start_at,
        end_at=end_at,
    )
    await message.answer(
        text="Интервал добавлен",
    )


# # get_user_and_availible_pages_intervals


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
# ):
#     users = await get_user_and_availible_pages_intervals_by_tg_id(
#         session=session,
#         user_tg_id=message.from_user.id,
#     )
#     for user in users:
#         await message.answer(
#             text=f"{user.id} - {user.username}",
#         )
#         for tg in user.tgs:
#             await message.answer(
#                 text=f"{tg.id}",
#             )
#         for page_interval in user.pages_intervals:
#             await message.answer(
#                 text=f"{page_interval.page_id} - {page_interval.interval_id}",
#             )
#             page = page_interval.page
#             interval = page_interval.interval
#             await message.answer(
#                 text=f"{page.id} - {page.vip}",
#             )
#             await message.answer(
#                 text=f"{interval.id} - {interval.start_at} - {interval.end_at}",
#             )


# # get_pages_available_to_user


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
# ):
#     pages = await get_pages_with_inter_users_tgs_by_user_tg_id(
#         session=session,
#         user_tg_id=message.from_user.id,
#     )
#     text = str()
#     for page in pages:
#         text += f"{page.id} - {page.vip}\n"
#         for page_interval_details in page.intervals_details:
#             text += f"-{page_interval_details.interval.start_at}\n"
#             if page_interval_details.user:
#                 text += f"--{page_interval_details.user.id}\n"
#                 for user_tgs in page_interval_details.user.tgs:
#                     text += f"---{user_tgs.id}\n"
#     await message.answer(
#         text=text,
#     )


# # add_page_user


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
# ):
#     page_user = message.text.split("-")
#     await add_page_user(
#         session=session,
#         page_id=int(page_user[0]),
#         user_id=int(page_user[1]),
#     )
#     await message.answer(
#         text=f"Связь {message.text} добавлена",
#     )


# # add_page_interval


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
# ):
#     page_interval = message.text.split("-")
#     await add_page_interval(
#         session=session,
#         page_id=int(page_interval[0]),
#         interval_id=int(page_interval[1]),
#     )
#     await message.answer(
#         text=f"Связь {message.text} добавлена",
#     )


# add_page


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
# ):
#     match message.text:
#         case "vip":
#             vip = True
#         case "free":
#             vip = False
#         case _:
#             vip = None
#     await add_page(
#         session=session,
#         model_id=1,
#         vip=vip,
#         sales_commission=20,
#     )
#     await message.answer(
#         text=f"Страница {message.text} добавлена",
#     )


# add_model


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
#     agency_id: int,
# ):
#     await add_model(
#         session=session,
#         agency_id=agency_id,
#         model_title=message.text,
#     )
#     await message.answer(
#         text=f"Модель {message.text} добавлена",
#     )


# Этот хэндлер будет реагировать на любые сообщения пользователя,
# не предусмотренные логикой работы бота
# @router.message(StateFilter(default_state))
# async def send_echo(message: Message):
#     await message.answer(LEXICON_RU['other'])
