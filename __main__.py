from aiogram import executor, types
from bot import dp
from genius.genius_request import *
from genius.genius_fsm import *


@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer("Привет!")


@dp.message_handler(commands=["get_song_lyrics"])
async def get_song(msg: types.Message):
    res = await search_song(msg.text)
    await msg.answer(res)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)