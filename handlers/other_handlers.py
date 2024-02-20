from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

# from lexicon.lexicon_ru import LEXICON_RU
from db.requests.with_add import (
    add_page_user,
)
from db.requests.with_add import add_interval, add_model, add_page, add_page_interval
from db.requests.with_page import get_all_pages_with_intervals_and_with_users_tgs
from db.models import PagesIntervalsORM

router = Router()

# get_pages_available_to_user


@router.message(StateFilter(default_state))
async def send_echo(
    message: Message,
    session: AsyncSession,
):
    pages = await get_all_pages_with_intervals_and_with_users_tgs(
        session=session,
        user_id=message.from_user.id,
    )
    for page in pages:
        await message.answer(
            text=f"{page.id} - {page.vip}",
        )
        for page_interval_details in page.intervals_details:
            await message.answer(
                text=f"{page_interval_details.interval.start_at}",
            ),
        for page_user_details in page.users_details:
            await message.answer(
                text=f"{page_user_details.user.id}",
            )
            for user_tgs in page_user_details.user.tgs:
                await message.answer(
                    text=f"{user_tgs.id}",
                )


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


# # add_interval


# @router.message(StateFilter(default_state))
# async def send_echo(
#     message: Message,
#     session: AsyncSession,
# ):
#     interval = message.text.split("-")
#     await add_interval(
#         session=session,
#         start_at=interval[0],
#         end_at=interval[1],
#     )
#     await message.answer(
#         text=f"Интервал {message.text} добавлен",
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
