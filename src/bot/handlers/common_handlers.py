from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from src.api.requester import Api
from src.bot.keyboards.default import default_kb_gen
from src.bot.keyboards.language import language_kb
from src.bot.text import Text
from src.db.dals import UserDAL
from src.db.models import User

# from src.bot.keyboards.default import kz_default_kb


def register_common_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def start_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
        await msg.answer(Text.welcome, reply_markup=language_kb)

    @dp.message(lambda msg: msg.text == "Русский")
    async def russian_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
        await user_dal.update_user(msg.from_user.id, language="ru")
        await msg.answer(
            _(Text.language_change, locale="ru"),
            reply_markup=default_kb_gen(locale="ru"),
        )

    @dp.message(lambda msg: msg.text == "Қазақ")
    async def kazakh_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
        await user_dal.update_user(msg.from_user.id, language="kk")
        await msg.answer(
            _(Text.language_change, locale="kk"),
            reply_markup=default_kb_gen(locale="kk"),
        )
