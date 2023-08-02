from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiohttp.web_exceptions import HTTPNotFound

from src.api.exceptions import ServerError
from src.api.requester import Api
from src.bot.handlers.common_handlers import register_common_handlers
from src.bot.handlers.settings_handlers import register_settings
from src.bot.handlers.settings_handlers import register_settings_handlers
from src.bot.keyboards.settings import settings_kb_gen
from src.bot.text import Text
from src.db.dals import UserDAL
from src.db.models import User


def register_handlers(dp: Dispatcher):
    register_common_handlers(dp)
    register_russian_handlers(dp)
    register_settings(dp)
    register_settings_handlers(dp)


def register_russian_handlers(dp: Dispatcher):
    @dp.message(lambda msg: msg.text == __(Text.settings_btn))
    async def ru_settings_message_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        await msg.answer(_(Text.settings_menu), reply_markup=settings_kb_gen())

    @dp.message(lambda msg: msg.text == __(Text.test_result_btn))
    async def ru_get_grant_results(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        try:
            data = await user_dal.get_cached(msg.from_user.id, user)
            if data:
                res = data

            else:
                res, status = await api.get_grant_result(user)
                res |= {"status": status}
                await user_dal.cache(msg.from_user.id, user, res)
            if res.get("status", 0) == 404:
                raise HTTPNotFound()
        except ValueError:
            await msg.answer(_(Text.field_required))
        except HTTPNotFound:
            await msg.answer(_(Text.results_not_found))
        except ServerError as ex:
            print(ex)
            await msg.answer(_(Text.server_error))
        else:
            await msg.answer(str(res))
