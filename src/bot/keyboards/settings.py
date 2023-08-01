from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


# RU LANG

type = KeyboardButton("Указать тип теста")
year = KeyboardButton("Указать год")
iin = KeyboardButton("Указать ИИН")
ikt = KeyboardButton("Указать ИКТ")
cancel = KeyboardButton("Отмена")

ru_settings_kb = (
    ReplyKeyboardMarkup(resize_keyboard=True).row(type, year, iin, ikt).add(cancel)
)

back = KeyboardButton("Назад")
ru_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(back)


ent = KeyboardButton("ЕНТ/КТ")
mag = KeyboardButton("Магистратура/Докторантура")
nkt = KeyboardButton("НКТ")
ru_type_kb = (
    ReplyKeyboardMarkup(resize_keyboard=True).add(ent).add(mag).add(nkt).add(back)
)
