from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.bot.keyboards.default import default_kb_gen
from src.bot.keyboards.language import language_kb
from src.bot.keyboards.settings import cancel_kb_gen
from src.bot.keyboards.settings import delete_me_kb_gen
from src.bot.keyboards.settings import settings_kb_gen
from src.bot.keyboards.settings import type_kb_gen
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.UserDAO import UserDAO

settings_router = Router(name="settings")


@settings_router.message(F.text == __(Text.cancel))
async def cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(_(Text.cancel), reply_markup=default_kb_gen())


@settings_router.message(F.text == __(Text.back))
async def back(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(_(Text.back), reply_markup=settings_kb_gen())


@settings_router.message(States.set_type)
async def set_type_handler(msg: Message, user_dal: UserDAO, state: FSMContext):
    if msg.text.strip() not in [
        _(Text.set_ent_btn),
        _(Text.set_mag_btn),
        _(Text.set_nkt_btn),
    ]:
        await msg.answer(_(Text.set_type_error_by_user), reply_markup=type_kb_gen())
        return
    if msg.text.strip() == _(Text.set_ent_btn):
        test_type = 1
    elif msg.text.strip() == _(Text.set_mag_btn):
        test_type = 2
    else:
        test_type = 3
    await user_dal.set_type(test_type)
    await msg.answer(_(Text.set_type_success), reply_markup=settings_kb_gen())
    await state.clear()


@settings_router.message(States.set_year)
async def set_year_handler(msg: Message, user_dal: UserDAO, state: FSMContext):
    try:
        value = int(msg.text.strip())
    except ValueError:
        msg.answer(_(Text.set_year_error_by_user))
    else:
        await user_dal.set_year(value)
        await msg.answer(_(Text.set_year_success), reply_markup=settings_kb_gen())
        await state.clear()


@settings_router.message(States.set_iin)
async def set_iin_handler(msg: Message, user_dal: UserDAO, state: FSMContext):
    try:
        iin = msg.text.strip()
        assert len(iin) == 12
        # TODO: make fully assert iin: "qwertyuiopas" also works
    except AssertionError:
        await msg.answer(_(Text.set_iin_error_by_user))
    else:
        await user_dal.set_iin(iin)
        await msg.answer(_(Text.set_iin_success), reply_markup=settings_kb_gen())
        await state.clear()


@settings_router.message(States.set_ikt)
async def set_ikt_handler(msg: Message, user_dal: UserDAO, state: FSMContext):
    try:
        ikt = msg.text.strip()
        assert len(ikt) == 9
        # TODO: make fully assert ikt: "qwertyuio" also works
    except AssertionError:
        await msg.answer(_(Text.set_ikt_error_by_user))
    else:
        await user_dal.set_ikt(ikt)
        await msg.answer(_(Text.set_ikt_success), reply_markup=settings_kb_gen())
        await state.clear()


@settings_router.message(F.text == __(Text.delete_me_btn))
async def delete_me(msg: Message, state: FSMContext):
    await state.set_state(States.delete_me)
    await msg.answer(_(Text.delete_ask), reply_markup=delete_me_kb_gen())


@settings_router.message(
    States.delete_me,
    F.text == __(Text.confirm_deletion_btn),
)
async def confirmed_deletion(msg: Message, user_dal: UserDAO, state: FSMContext):
    await user_dal.delete_user()
    await msg.answer(_(Text.delete_success), reply_markup=language_kb)
    await state.clear()


@settings_router.message(F.text == __(Text.set_type_btn))
async def set_type(msg: Message, state: FSMContext):
    await state.set_state(States.set_type)
    await msg.answer(_(Text.set_type), reply_markup=type_kb_gen())


@settings_router.message(F.text == __(Text.set_year_btn))
async def set_year(msg: Message, state: FSMContext):
    await state.set_state(States.set_year)
    await msg.answer(_(Text.set_year), reply_markup=cancel_kb_gen())


@settings_router.message(F.text == __(Text.set_iin_btn))
async def set_iin(msg: Message, state: FSMContext):
    await state.set_state(States.set_iin)
    await msg.answer(_(Text.set_iin), reply_markup=cancel_kb_gen())


@settings_router.message(F.text == __(Text.set_ikt_btn))
async def set_ikt(msg: Message, state: FSMContext):
    await state.set_state(States.set_ikt)
    await msg.answer(_(Text.set_ikt), reply_markup=cancel_kb_gen())


@settings_router.message(F.text == __(Text.set_change_lang_btn))
async def change_lang(msg: Message):
    await msg.answer(_(Text.welcome), reply_markup=language_kb)
