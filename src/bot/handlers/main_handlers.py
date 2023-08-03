from aiogram.dispatcher.router import Router
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiohttp.web_exceptions import HTTPNotFound

from src.api.exceptions import ServerError
from src.api.requester import Api
from src.bot.keyboards.info import info_kb_gen
from src.bot.keyboards.settings import settings_kb_gen
from src.bot.text import Text
from src.db.dals import UserDAL


main_router = Router(name="main")


@main_router.message(lambda msg: msg.text == __(Text.settings_btn))
async def settings_message_handler(msg: Message):
    await msg.answer(_(Text.settings_menu), reply_markup=settings_kb_gen())


@main_router.message(lambda msg: msg.text == __(Text.test_result_btn))
async def get_grant_results(msg: Message, user_dal: UserDAL, api: Api):
    try:
        data = await user_dal.get_cached()
        if data:
            res = data

        else:
            res, status = await api.get_grant_result(user_dal)
            res |= {"status": status}
            await user_dal.cache(res)
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


@main_router.message(lambda msg: msg.text == __(Text.info_btn))
async def info_message_handler(msg: Message):
    await msg.answer(_(Text.info_btn), reply_markup=info_kb_gen())
