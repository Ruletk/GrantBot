from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import Redis
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n

from src.bot.middlewares import CustomI18NMiddleware
from src.bot.middlewares import ResourceMiddleware
from src.bot.middlewares import UserMiddleware
from src.settings import BOT_TOKEN
from src.settings import REDIS_HOST
from src.settings import REDIS_PASSWORD
from src.settings import REDIS_PORT


redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
redis_storage = RedisStorage(redis)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=redis_storage)

i18n = I18n(path="locales", default_locale="kk", domain="messages")


ResourceMiddleware().setup(dp)
UserMiddleware().setup(dp)
CustomI18NMiddleware(i18n=i18n).setup(dp)


from src.bot.handlers import router

dp.include_router(router)
