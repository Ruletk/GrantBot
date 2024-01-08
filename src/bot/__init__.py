from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n

from src.bot.middlewares import CustomI18NMiddleware
from src.bot.middlewares import ResourceMiddleware
from src.bot.middlewares import UserMiddleware
from src.settings import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

i18n = I18n(path="locales", default_locale="kk", domain="messages")


dp.message.outer_middleware(ResourceMiddleware())
dp.message.outer_middleware(UserMiddleware())


CustomI18NMiddleware(i18n=i18n).setup(dp)


from src.bot.handlers import router

dp.include_router(router)
