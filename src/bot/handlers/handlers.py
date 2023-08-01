from aiogram import Dispatcher
from aiogram.types import Message
from aiohttp.web_exceptions import HTTPNotFound

from src.api.exceptions import ServerError
from src.api.requester import Api
from src.bot.handlers.common_handlers import register_common_handlers
from src.bot.handlers.settings_handlers import register_settings
from src.bot.handlers.settings_handlers import register_settings_handlers
from src.bot.keyboards.settings import ru_settings_kb
from src.bot.messages import messages
from src.db.dals import UserDAL
from src.db.models import User


def register_handlers(dp: Dispatcher):
    register_common_handlers(dp)
    register_russian_handlers(dp)
    register_settings(dp)
    register_settings_handlers(dp)


def register_russian_handlers(dp: Dispatcher):
    @dp.message_handler(lambda msg: msg.text == "Настройки")
    async def ru_settings_message_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        await msg.answer("Меню настроек", reply_markup=ru_settings_kb)

    @dp.message_handler(lambda msg: msg.text == "Получить результат")
    async def ru_get_grant_results(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        try:
            res = await api.get_grant_result(user)
            await msg.answer(res)
        except ValueError:
            await msg.answer(messages["ru_field_request"])
        except HTTPNotFound:
            await msg.answer(messages["ru_results_not_found"])
        except ServerError as ex:
            print(ex)
            await msg.answer(messages["ru_server_error"])
