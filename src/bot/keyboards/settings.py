from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup


# RU LANG

type = KeyboardButton(text="Указать тип теста")
year = KeyboardButton(text="Указать год")
iin = KeyboardButton(text="Указать ИИН")
ikt = KeyboardButton(text="Указать ИКТ")
cancel = KeyboardButton(text="Отмена")

ru_settings_kb = ReplyKeyboardMarkup(
    keyboard=[[type, year, iin, ikt], [cancel]], resize_keyboard=True
)

back = KeyboardButton(text="Назад")
ru_cancel_kb = ReplyKeyboardMarkup(keyboard=[[back]], resize_keyboard=True)


ent = KeyboardButton(text="ЕНТ/КТ")
mag = KeyboardButton(text="Магистратура/Докторантура")
nkt = KeyboardButton(text="НКТ")
ru_type_kb = ReplyKeyboardMarkup(keyboard=[[ent, mag, nkt, back]], resize_keyboard=True)
