from bot import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from genius.genius_request import search_song

class Lyrics_handler(StatesGroup):
    wait_artist = State()
    wait_song = State()

@dp.message_handler(Text(equals="Найти трек"))
async def start_search(message: types.Message):
    await Lyrics_handler.wait_artist.set()
    await message.answer('Введи исполнителя:')

@dp.message_handler(state=Lyrics_handler.wait_artist)
async def wait_artist(message: types.Message, state: FSMContext):
    artist = message.text
    await state.update_data(artist=artist)
    await Lyrics_handler.next() 
    await message.answer("Теперь введи название песни:")

@dp.message_handler(state=Lyrics_handler.wait_song)
async def wait_song(message: types.Message, state: FSMContext):
    data = await state.get_data()
    artist = data.get('artist')
    song = message.text
    await message.answer("Готово, вот трек, который ты искал:")
    song_lyrics = await search_song(song, artist)
    await message.answer(song_lyrics)
    await state.finish()