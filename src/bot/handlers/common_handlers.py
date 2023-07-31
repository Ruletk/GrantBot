from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from src.bot.keyboards.language import language_kb
from src.bot.keyboards.default import ru_default_kb, kz_default_kb
from src.db.dals import UserDAL
from src.bot.messages import messages
from src.db.models import User
from src.api.requester import Api


def register_common_handlers(dp: Dispatcher):
    @dp.message_handler(Command("start"))
    async def start_message_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        await msg.answer(messages["welcome"], reply_markup=language_kb)

    @dp.message_handler(lambda msg: msg.text == "Русский")
    async def russian_message_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        await user_dal.update_user(msg.from_user.id, language="ru")
        await msg.answer(messages["ru_default"], reply_markup=ru_default_kb)

    @dp.message_handler(lambda msg: msg.text == "Қазақ")
    async def kazakh_message_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api
    ):
        await user_dal.update_user(msg.from_user.id, language="kz")
        await msg.answer(messages["kz_default"], reply_markup=kz_default_kb)
