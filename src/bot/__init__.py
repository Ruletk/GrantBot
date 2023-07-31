from aiogram import Bot
from aiogram import Dispatcher

from src.bot.middlewares import ResourceMiddleware
from src.bot.middlewares import UserMiddlwware
from src.settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


dp.middleware.setup(ResourceMiddleware())
dp.middleware.setup(UserMiddlwware())


from .handlers.handlers import register_handlers

register_handlers(dp)
