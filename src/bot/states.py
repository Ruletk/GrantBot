from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup


class States(StatesGroup):
    list_grants = State()
    create_grant = State()
    set_type = State()
    set_ikt = State()
    set_iin = State()
    set_year = State()
    delete_me = State()
    confirm_policy = State()
