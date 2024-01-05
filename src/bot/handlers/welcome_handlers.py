from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from src.bot.keyboards.default import default_kb_gen
from src.bot.keyboards.default import privacy_kb_gen
from src.bot.keyboards.language import language_kb
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.UserDAO import UserDAO

welcome_router = Router(name="welcome")


@welcome_router.message(Command("start"))
async def start_message(msg: Message):
    await msg.answer(Text.welcome, reply_markup=language_kb)


@welcome_router.message(F.text == "Русский")
async def russian_message(msg: Message, user_dal: UserDAO, state: FSMContext):
    await user_dal.set_lang("ru")
    await state.set_state(States.confirm_policy)
    await msg.answer(
        _(Text.policy, locale="ru").format(bot=Text.bot_name),
        reply_markup=privacy_kb_gen(locale="ru"),
    )


@welcome_router.message(F.text == "Қазақ")
async def kazakh_message(msg: Message, user_dal: UserDAO, state: FSMContext):
    await user_dal.set_lang("kk")
    await state.set_state(States.confirm_policy)
    await msg.answer(
        _(Text.policy, locale="kk").format(bot=Text.bot_name),
        reply_markup=privacy_kb_gen(locale="kk"),
    )


@welcome_router.message(States.confirm_policy)
async def confirm_privacy(msg: Message, user_dal: UserDAO, state: FSMContext):
    if msg.text == _(Text.policy_btn_confirm):
        await user_dal.policy_confirm()
        await msg.answer(_(Text.policy_confirm_success), reply_markup=default_kb_gen())
        await state.clear()
