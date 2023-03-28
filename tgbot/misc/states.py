from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class GalleryState(StatesGroup):
    photo = State()


class ProfileState(StatesGroup):
    profile = State()


class AdminControlBalanceState(StatesGroup):
    check_balance = State()
    change_balance_get_id = State()
    change_balance = State()
    add_balance_get_id = State()
    add_balance = State()
    minus_balance_get_id = State()
    minus_balance = State()
