from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class GalleryState(StatesGroup):
    photo = State()


class ProfileState(StatesGroup):
    profile = State()

