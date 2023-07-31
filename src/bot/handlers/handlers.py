from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from src.bot.keyboards.language import language_kb
from src.bot.keyboards.default import ru_default_kb, kz_default_kb
from src.db.dals import UserDAL
from src.db.session import get_db
from src.bot.messages import messages


def register_handlers(dp: Dispatcher):
    @dp.message_handler(Command("start"))
    async def start_message_handler(msg: Message):
        user_dal = UserDAL(get_db())
        await user_dal.create_user(msg.from_user.id)
        await msg.answer(messages["welcome"], reply_markup=language_kb)

    @dp.message_handler(lambda msg: msg.text == "Русский")
    async def russian_message_handler(msg: Message):
        user_dal = UserDAL(get_db())
        await user_dal.update_user(msg.from_user.id, language="ru")
        await msg.answer(messages["ru_default"], reply_markup=ru_default_kb)

    @dp.message_handler(lambda msg: msg.text == "Қазақ")
    async def kazakh_message_handler(msg: Message):
        user_dal = UserDAL(get_db())
        await user_dal.update_user(msg.from_user.id, language="kz")
        await msg.answer(messages["kz_default"], reply_markup=kz_default_kb)


def register_russian_handlers(dp: Dispatcher):
    @dp.message_handler(lambda msg: msg.text == "Настройки")
    async def settings_message_handler(msg: Message):
        ...
