from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup


class States(StatesGroup):
    set_type = State()
    set_ikt = State()
    set_iin = State()
    set_year = State()
