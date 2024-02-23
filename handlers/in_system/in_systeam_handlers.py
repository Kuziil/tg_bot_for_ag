from zoneinfo import ZoneInfo

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.schedule.month.kb_month_schedule import create_schedule
from keyboards.kb_single_line_vertically import create_menu_keyboard
from handlers.in_system.schedules.month_handlers import schedule_router
from keyboards.schedule.month_v2.bilder import create_month_shudle_v2
from sqlalchemy.ext.asyncio import AsyncSession


in_systeam_router = Router()

in_systeam_router.include_router(schedule_router)


@in_systeam_router.callback_query(
    F.data == "schedule",
    StateFilter(default_state),
)
async def process_schedule_press(
    callback: CallbackQuery,
    i18n: dict[str, dict[str, str]],
):
    """Данный хэндлер отрабатывает на нажатие кнопки расписание ->
    выдает инлайн клавиатуру с типами расписания

    Args:
        callback (CallbackQuery): _description_
    """
    await callback.message.edit_text(
        text=i18n["lexicon"]["schedule_type"],
        reply_markup=create_menu_keyboard(
            "mounth_schedule",
            "week_schedule",
        ),
    )
    await callback.answer()


@in_systeam_router.callback_query(
    F.data == "mounth_schedule",
    StateFilter(default_state),
)
async def process_mounth_schedule_press(
    callback: CallbackQuery,
    i18n: dict[str, dict[str, str]],
):
    await callback.message.edit_text(
        text=i18n["lexicon"]["schedule"],
        reply_markup=create_schedule(),
    )
    await callback.answer()


@in_systeam_router.callback_query(
    F.data == "week_schedule",
    StateFilter(default_state),
)
async def process_mounth_schedule_press(
    callback: CallbackQuery,
    session: AsyncSession,
    i18n: dict[str, dict[str, str]],
    defult_tz: ZoneInfo,
):
    await callback.message.edit_text(
        text=i18n["lexicon"]["week_schedule"],
        reply_markup=await create_month_shudle_v2(
            session=session,
            user_tg_id=callback.from_user.id,
            i18n=i18n,
            defult_tz=defult_tz,
        ),
    )
    await callback.answer()


# @in_systeam_router.callback_query(
#     F.data == "week_schedule",
#     StateFilter(default_state),
# )
# async def process_mounth_schedule_press(
#     callback: CallbackQuery,
#     session: AsyncSession,
#     i18n: dict[str, dict[str, str]],
#     deafult_tz: ZoneInfo,
# ):
#     await callback.message.edit_text(
#         text=i18n["lexicon"]["week_schedule"],
#         reply_markup=await create_week_shudle(
#             session=session,
#             user_tg_id=callback.from_user.id,
#             i18n=i18n,
#             deafult_tz=deafult_tz,
#         ),
#     )
#     await callback.answer()
