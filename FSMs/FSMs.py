from aiogram.fsm.state import StatesGroup, State


class FSMFillForm(StatesGroup):
    fill_username = State()
    fill_emoji = State()
    fill_shifts = State()


class FSMSetShifts(StatesGroup):
    shifts = State()


class FSMFillReport(StatesGroup):
    page_interval_id = State()
    day = State()
    month = State()
    year = State()
    photos = State()
    dirty = State()
