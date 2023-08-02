from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


ru_button_settings = KeyboardButton(text="Настройки")
ru_button_get_result = KeyboardButton(text="Получить результат")


ru_default_kb = ReplyKeyboardMarkup(
    keyboard=[[ru_button_get_result, ru_button_settings]], resize_keyboard=True
)

# kz_button_settings = KeyboardButton("")
# kz_button_get_result = KeyboardButton("")

# kz_default_kb = ReplyKeyboardMarkup(
#     keyboard=[[kz_button_get_result, kz_button_settings]], resize_keyboard=True
# )
