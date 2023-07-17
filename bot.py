from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from util.constants import TELEGRAM_TOKEN

storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)