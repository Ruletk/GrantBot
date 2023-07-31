from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


ru_lang = KeyboardButton("Русский")
kz_lang = KeyboardButton("Қазақ")


language_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(ru_lang).add(kz_lang)
