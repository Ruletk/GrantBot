from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.bot.text import Text

info_router = Router(name="info")


@info_router.message(F.text == __(Text.policy_btn))
async def policy_handler(msg: Message):
    await msg.answer(_(Text.policy))
