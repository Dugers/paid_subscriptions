from aiogram.dispatcher.filters.state import StatesGroup, State


class UserAddBalanceState(StatesGroup):
    need_add = State()