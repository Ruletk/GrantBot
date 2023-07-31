from aiogram import Bot, Dispatcher
from src.settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


from .handlers.handlers import register_handlers

register_handlers(dp)
