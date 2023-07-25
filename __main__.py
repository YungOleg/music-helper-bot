from aiogram import executor
from init_bot import dp
from logger import log


async def on_startup(_):
    log.info("Bot started")


if __name__ == "__main__":
    executor.start_polling(
        dp, 
        skip_updates=True,
        on_startup=on_startup
        )