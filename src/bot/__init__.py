from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.middlewares import ResourceMiddleware
from src.bot.middlewares import UserMiddlwware
from src.settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(ResourceMiddleware())
dp.message.middleware(UserMiddlwware())


from .handlers.handlers import register_handlers

register_handlers(dp)
