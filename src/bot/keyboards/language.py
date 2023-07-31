from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


ru_lang = KeyboardButton("Русский")
kz_lang = KeyboardButton("Қазақ")


language_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(ru_lang).add(kz_lang)
