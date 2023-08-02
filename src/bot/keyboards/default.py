from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import get_i18n
from aiogram.utils.i18n import gettext as _

from src.bot.text import Text


def default_kb_gen(locale=None):
    if not locale:
        locale = get_i18n().current_locale
    button_settings = KeyboardButton(text=_(Text.settings_btn, locale=locale))
    button_get_result = KeyboardButton(text=_(Text.test_result_btn, locale=locale))

    return ReplyKeyboardMarkup(
        keyboard=[[button_get_result, button_settings]], resize_keyboard=True
    )
