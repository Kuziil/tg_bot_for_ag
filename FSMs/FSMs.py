from aiogram.fsm.state import StatesGroup, State


class FSMFillForm(StatesGroup):
    fill_username = State()
    fill_emoticon = State()
    fiil_shifts = State()


class FSMSetShifts(StatesGroup):
    shifts = State()
