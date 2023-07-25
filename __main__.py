from aiogram import executor
from init_bot import dp
from logger import log
from handlers import *

async def on_startup(_):
    log.info("Bot started")


if __name__ == "__main__":
    executor.start_polling(
        dp, 
        skip_updates=True,
        on_startup=on_startup
        )


#? TODO list
# TODO Можно получать bpm трека, а также его тональкость
# TODO Сделать меню информации о треке(bpm, тональность)
# TODO перенести все вспомогательные функции в middlware
# TODO перевод трека сделать в стиле: строчка на английском(жирным шрифтом), потом ее перевод обычным текстом (для этого нужно сделать отдельную функцию: )
# TODO сделать скачивание всего альбома
# TODO добавить скачивание мп3 с ютуба
# TODO переименовать бота в music hepler bot
# ! TODO переделывать функцию скачивания