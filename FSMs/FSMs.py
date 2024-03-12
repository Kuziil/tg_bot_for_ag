from aiogram.fsm.state import StatesGroup, State


class FSMFillForm(StatesGroup):
    fill_username = State()
    fill_emoticon = State()
    fill_shifts = State()


class FSMSetShifts(StatesGroup):
    shifts = State()


class FSMFillReport(StatesGroup):
    page_interval_id = State()
    photos = State()
    dirty = State()
