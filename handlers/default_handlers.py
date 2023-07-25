from init_bot import dp
from keyboards.keyboards import open_menu_keyboard, menu_keyboard
from aiogram import types


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет!", reply_markup=open_menu_keyboard)
    await message.delete()


@dp.message_handler(text="Открыть меню")
async def main_menu(message: types.Message):
    await message.answer(
        "Ты находишься в главном меню. Выбери действие, которое хочешь совершить:",
        reply_markup=menu_keyboard
    )
    await message.delete()