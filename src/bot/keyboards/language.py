from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup

from src.bot.callback import SettingsCallback

ru_lang = KeyboardButton(text="Русский язык")
kz_lang = KeyboardButton(text="Қазақ тілі")

language_kb = ReplyKeyboardMarkup(keyboard=[[ru_lang, kz_lang]], resize_keyboard=True)


async def language_kb_gen():
    ru = InlineKeyboardButton(
        text="Русский язык",
        callback_data=SettingsCallback(action="change_lang", lang="ru").pack(),
    )
    kz = InlineKeyboardButton(
        text="Қазақ тілі",
        callback_data=SettingsCallback(action="change_lang", lang="kk").pack(),
    )
    return InlineKeyboardMarkup(inline_keyboard=[[ru], [kz]])
