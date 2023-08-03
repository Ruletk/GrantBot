from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from src.api.requester import Api
from src.bot.keyboards.default import default_kb_gen
from src.bot.keyboards.language import language_kb
from src.bot.text import Text
from src.db.dals import UserDAL
from src.db.models import User


welcome_router = Router(name="welcome")


@welcome_router.message(Command("start"))
async def start_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
    await msg.answer(Text.welcome, reply_markup=language_kb)


@welcome_router.message(lambda msg: msg.text == "Русский")
async def russian_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
    await user_dal.update_user(msg.from_user.id, language="ru")
    await msg.answer(
        _(Text.policy, locale="ru"),
        reply_markup=default_kb_gen(locale="ru"),
    )


@welcome_router.message(lambda msg: msg.text == "Қазақ")
async def kazakh_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
    await user_dal.update_user(msg.from_user.id, language="kk")
    await msg.answer(
        _(Text.policy, locale="kk"),
        reply_markup=default_kb_gen(locale="kk"),
    )
