from aiogram.fsm.state import StatesGroup, State


class MySG(StatesGroup):
    menu = State()
    enter_city = State()
    rps = State()