from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from src.api.requester import Api
from src.bot.keyboards.default import ru_default_kb
from src.bot.keyboards.language import language_kb
from src.bot.messages import messages
from src.db.dals import UserDAL
from src.db.models import User

# from src.bot.keyboards.default import kz_default_kb


def register_common_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def start_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
        await msg.answer(messages["welcome"], reply_markup=language_kb)

    @dp.message(lambda msg: msg.text == "Русский")
    async def russian_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
        await user_dal.update_user(msg.from_user.id, language="ru")
        await msg.answer(messages["ru_default"], reply_markup=ru_default_kb)

    @dp.message(lambda msg: msg.text == "Қазақ")
    async def kazakh_message(msg: Message, user: User, user_dal: UserDAL, api: Api):
        await user_dal.update_user(msg.from_user.id, language="kz")
        await msg.answer(messages["kz_default"])
        # await msg.answer(messages["kz_default"], reply_markup=kz_default_kb)
