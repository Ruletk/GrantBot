from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


ru_button_settings = KeyboardButton("Настройки")
ru_button_get_result = KeyboardButton("Получить результат")


ru_default_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    ru_button_get_result, ru_button_settings
)

kz_button_settings = KeyboardButton("")
kz_button_get_result = KeyboardButton("")

kz_default_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    kz_button_get_result, kz_button_settings
)
