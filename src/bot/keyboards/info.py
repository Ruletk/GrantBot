from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import get_i18n
from aiogram.utils.i18n import gettext as _

from src.bot.text import Text


async def info_kb_gen(locale=None):
    if not locale:
        locale = get_i18n().current_locale
    cancel = KeyboardButton(text=_(Text.cancel))
    button_policy = KeyboardButton(text=_(Text.policy_btn, locale=locale))

    return ReplyKeyboardMarkup(
        keyboard=[[button_policy], [cancel]], resize_keyboard=True
    )
