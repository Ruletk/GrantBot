from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


ru_lang = KeyboardButton(text="Русский")
kz_lang = KeyboardButton(text="Қазақ")


language_kb = ReplyKeyboardMarkup(keyboard=[[ru_lang, kz_lang]], resize_keyboard=True)
