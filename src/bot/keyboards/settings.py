from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from src.bot.text import Text


# # RU LANG


def settings_kb_gen():
    type = KeyboardButton(text=_(Text.set_type_btn))
    year = KeyboardButton(text=_(Text.set_year_btn))
    iin = KeyboardButton(text=_(Text.set_iin_btn))
    ikt = KeyboardButton(text=_(Text.set_ikt_btn))
    change_lang = KeyboardButton(text=_(Text.set_change_lang_btn))
    cancel = KeyboardButton(text=_(Text.cancel))

    return ReplyKeyboardMarkup(
        keyboard=[[type, year, iin, ikt], [change_lang], [cancel]], resize_keyboard=True
    )


def cancel_kb_gen():
    back = KeyboardButton(text=_(Text.back))
    return ReplyKeyboardMarkup(keyboard=[[back]], resize_keyboard=True)


def type_kb_gen():
    back = KeyboardButton(text=_(Text.back))
    ent = KeyboardButton(text=_(Text.set_ent_btn))
    mag = KeyboardButton(text=_(Text.set_mag_btn))
    nkt = KeyboardButton(text=_(Text.set_nkt_btn))
    return ReplyKeyboardMarkup(keyboard=[[ent, mag, nkt, back]], resize_keyboard=True)
