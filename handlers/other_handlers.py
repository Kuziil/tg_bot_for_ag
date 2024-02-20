from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

# from lexicon.lexicon_ru import LEXICON_RU
from db.requests import add_model, add_page, add_interval

router = Router()

# add_interval


@router.message(StateFilter(default_state))
async def send_echo(
    message: Message,
    session: AsyncSession,
):
    interval = message.text.split("-")
    await add_interval(
        session=session,
        start_at=interval[0],
        end_at=interval[1],
    )
    await message.answer(
        text=f"Интервал {message.text} добавлен",
    )


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
