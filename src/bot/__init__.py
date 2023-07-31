from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from src.settings import BOT_TOKEN
from src.bot.middlewares import ResourceMiddleware, UserMiddlwware


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


dp.middleware.setup(ResourceMiddleware())
dp.middleware.setup(UserMiddlwware())


from .handlers.handlers import register_handlers

register_handlers(dp)
