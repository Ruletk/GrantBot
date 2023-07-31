from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.dals import UserDAL
from src.db.models import User
from src.api.requester import Api
from src.api.exceptions import ServerError
from src.bot.handlers.common_handlers import register_common_handlers
from src.bot.messages import messages
from aiohttp.web_exceptions import HTTPNotFound


def register_handlers(dp: Dispatcher):
    register_common_handlers(dp)
    register_russian_handlers(dp)


def register_russian_handlers(dp: Dispatcher):
    @dp.message_handler(lambda msg: msg.text == "Настройки")
    async def ru_settings_message_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        ...

    @dp.message_handler(lambda msg: msg.text == "Получить результат")
    async def ru_get_grant_results(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        try:
            res = await api.get_grant_result(user)
            await msg.answer(res)
        except HTTPNotFound:
            await msg.answer(messages["ru_results_not_found"])
        except ServerError as ex:
            print(ex)
            await msg.answer(messages["ru_server_error"])
