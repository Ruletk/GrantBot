from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.bot.callback import CancelCallback
from src.bot.keyboards.default import default_kb_gen
from src.bot.keyboards.language import language_kb
from src.bot.keyboards.settings import delete_me_kb_gen
from src.bot.keyboards.settings import settings_kb_gen
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.UserDAO import UserDAO

settings_router = Router(name="settings")


@settings_router.message(F.text == __(Text.cancel))
async def cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(_(Text.cancel), reply_markup=default_kb_gen())


@settings_router.callback_query(CancelCallback.filter(F.cancel == "cancel"))
async def cancel_query(query, state: FSMContext):
    await state.clear()
    await query.message.answer(_(Text.cancel), reply_markup=default_kb_gen())


@settings_router.message(F.text == __(Text.back))
async def back(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(_(Text.back), reply_markup=await settings_kb_gen())


@settings_router.message(F.text == __(Text.delete_me_btn))
async def delete_me(msg: Message, state: FSMContext):
    await state.set_state(States.delete_me)
    await msg.answer(_(Text.delete_ask), reply_markup=delete_me_kb_gen())


@settings_router.message(
    States.delete_me,
    F.text == __(Text.confirm_deletion_btn),
)
async def confirmed_deletion(msg: Message, user_dao: UserDAO, state: FSMContext):
    await user_dao.delete_user()
    await msg.answer(_(Text.delete_success), reply_markup=language_kb)
    await state.clear()


@settings_router.message(F.text == __(Text.set_change_lang_btn))
async def change_lang(msg: Message):
    await msg.answer(_(Text.welcome), reply_markup=language_kb)
