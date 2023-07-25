from aiogram.dispatcher.filters.state import State, StatesGroup


class Find_album(StatesGroup):
    wait_artist = State()