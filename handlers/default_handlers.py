from init_bot import dp
from keyboards.keyboards import open_menu_keyboard
from aiogram import types


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет!", reply_markup=open_menu_keyboard)
    await message.delete()