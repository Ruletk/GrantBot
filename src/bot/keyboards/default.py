from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import get_i18n
from aiogram.utils.i18n import gettext as _

from src.bot.text import Text


def privacy_kb_gen(locale=None):
    if not locale:
        locale = get_i18n().current_locale
    button_confirm = KeyboardButton(text=_(Text.policy_btn_confirm, locale=locale))
    return ReplyKeyboardMarkup(keyboard=[[button_confirm]], resize_keyboard=True)


def default_kb_gen(locale=None):
    if not locale:
        locale = get_i18n().current_locale
    button_settings = KeyboardButton(text=_(Text.settings_btn, locale=locale))
    button_get_result = KeyboardButton(text=_(Text.test_result_btn, locale=locale))
    button_info = KeyboardButton(text=_(Text.info_btn, locale=locale))

    return ReplyKeyboardMarkup(
        keyboard=[[button_get_result, button_settings], [button_info]],
        resize_keyboard=True,
    )


async def download_link_kb_gen(url, locale=None):
    if not locale:
        locale = get_i18n().current_locale
    download_link = InlineKeyboardButton(
        text=_(Text.download_link_btn, locale=locale), url=url
    )
    return InlineKeyboardMarkup(inline_keyboard=[[download_link]])
