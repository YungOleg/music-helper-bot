from bot import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class Lyrics_handler(StatesGroup):
    wait_artist = State()
    wait_song = State()

@dp.message_handler(state=Lyrics_handler.wait_artist)
async def wait_artist(message: types.Message, state: FSMContext):
    ...