from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n

from src.bot.middlewares import CustomI18NMiddleware
from src.bot.middlewares import ResourceMiddleware
from src.bot.middlewares import UserMiddlwware
from src.settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

i18n = I18n(path="locales", default_locale="kk", domain="messages")


dp.message.outer_middleware(ResourceMiddleware())
dp.message.outer_middleware(UserMiddlwware())
dp.message.outer_middleware(CustomI18NMiddleware(i18n=i18n))


from .handlers.handlers import register_handlers

register_handlers(dp)
