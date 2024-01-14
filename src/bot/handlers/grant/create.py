from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from src.bot.callback import CancelCallback
from src.bot.callback import CreateGrantCallback
from src.bot.callback import SelectTestTypeCallback
from src.bot.callback import SettingsCallback
from src.bot.keyboards.settings import create_grant_kb_gen
from src.bot.keyboards.settings import create_test_type_kb_gen
from src.bot.keyboards.settings import grant_list_kb_gen
from src.bot.keyboards.settings import inline_cancel_kb_gen
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.GrantDAO import GrantDAO
from src.db.dao.UserDAO import UserDAO
from src.db.models.Grant import Grant
from src.miscs.validators import validate_iin
from src.miscs.validators import validate_ikt
from src.miscs.validators import validate_year

create_router = Router(name="create")


@create_router.callback_query(SettingsCallback.filter(F.action == "create_grant"))
async def create_result(callback, state: FSMContext, user_dao: UserDAO):
    if len(await user_dao.get_grants()) >= 2:
        await callback.message.bot.edit_message_text(
            _(Text.grants_limit),
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
        )
        return
    await state.set_state(States.create_grant)

    await callback.message.bot.edit_message_text(
        _(Text.create_grant),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await create_grant_kb_gen(state),
    )


@create_router.callback_query(CancelCallback.filter(F.cancel_type == "create_grant"))
async def create_grant_cancel_handler(query, state: FSMContext, user_dao: UserDAO):
    await query.message.bot.edit_message_text(
        _(Text.create_grant, locale=await user_dao.get_user_language()),
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=await create_grant_kb_gen(state),
    )
    await state.set_state(States.create_grant)


@create_router.callback_query(CreateGrantCallback.filter(F.type_ == "iin"))
async def create_grant_iin_handler(query, state: FSMContext):
    if await state.get_state() != States.create_grant.state:
        return
    await query.message.bot.edit_message_text(
        _(Text.set_iin),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await inline_cancel_kb_gen("create_grant"),
    )
    await state.set_state(States.set_iin)


@create_router.callback_query(CreateGrantCallback.filter(F.type_ == "ikt"))
async def create_grant_ikt_handler(query, state: FSMContext):
    if await state.get_state() != States.create_grant.state:
        return
    await query.message.bot.edit_message_text(
        _(Text.set_ikt),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await inline_cancel_kb_gen("create_grant"),
    )
    await state.set_state(States.set_ikt)


@create_router.callback_query(CreateGrantCallback.filter(F.type_ == "year"))
async def create_grant_year_handler(query, state: FSMContext):
    if await state.get_state() != States.create_grant.state:
        return
    await query.message.bot.edit_message_text(
        _(Text.set_year),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await inline_cancel_kb_gen("create_grant"),
    )
    await state.set_state(States.set_year)


@create_router.callback_query(CreateGrantCallback.filter(F.type_ == "test_type"))
async def create_grant_test_type_handler(query, state: FSMContext):
    if await state.get_state() != States.create_grant.state:
        return
    await query.message.bot.edit_message_text(
        _(Text.set_type),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await create_test_type_kb_gen(),
    )


@create_router.message(States.set_iin)
async def create_grant_set_iin(msg: Message, state: FSMContext, user_dao: UserDAO):
    iin = msg.text.strip()
    await msg.delete()

    data = await state.get_data()

    if not validate_iin(iin):
        await msg.bot.edit_message_text(
            _(Text.set_iin_error_by_user),
            chat_id=msg.chat.id,
            message_id=data.get("root_message_id"),
            reply_markup=await inline_cancel_kb_gen("create_grant"),
        )
        return

    await state.update_data({"iin": iin, "iin_check": True})

    if await create_grant(msg, state, user_dao):
        return

    await msg.bot.edit_message_text(
        _(Text.set_iin_success),
        chat_id=msg.chat.id,
        message_id=data.get("root_message_id"),
        reply_markup=await create_grant_kb_gen(state),
    )
    await state.set_state(States.create_grant)


@create_router.message(States.set_ikt)
async def create_grant_set_ikt(msg: Message, state: FSMContext, user_dao: UserDAO):
    await msg.delete()
    ikt = msg.text.strip()
    data = await state.get_data()

    if not validate_ikt(ikt):
        await msg.bot.edit_message_text(
            _(Text.set_ikt_error_by_user),
            chat_id=msg.chat.id,
            message_id=data.get("root_message_id"),
            reply_markup=await inline_cancel_kb_gen("create_grant"),
        )
        return

    await state.update_data({"ikt": ikt, "ikt_check": True})

    if await create_grant(msg, state, user_dao):
        return

    await msg.bot.edit_message_text(
        _(Text.set_ikt_success),
        chat_id=msg.chat.id,
        message_id=data.get("root_message_id"),
        reply_markup=await create_grant_kb_gen(state),
    )
    await state.set_state(States.create_grant)


@create_router.message(States.set_year)
async def create_grant_set_year(msg: Message, state: FSMContext, user_dao: UserDAO):
    await msg.delete()
    year = msg.text.strip()
    data = await state.get_data()

    if not validate_year(year):
        await msg.bot.edit_message_text(
            _(Text.set_year_error_by_user),
            chat_id=msg.chat.id,
            message_id=data.get("root_message_id"),
            reply_markup=await inline_cancel_kb_gen("create_grant"),
        )
        return

    await state.update_data({"year": year, "year_check": True})

    if await create_grant(msg, state, user_dao):
        return

    await msg.bot.edit_message_text(
        _(Text.set_year_success),
        chat_id=msg.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await create_grant_kb_gen(state),
    )
    await state.set_state(States.create_grant)


@create_router.callback_query(SelectTestTypeCallback.filter(F.type_ == "ent"))
async def create_grant_ent_select(query, state: FSMContext, user_dao: UserDAO):
    await set_type(query, state, 1, user_dao)


@create_router.callback_query(SelectTestTypeCallback.filter(F.type_ == "mag"))
async def create_grant_mag_select(query, state: FSMContext, user_dao: UserDAO):
    await set_type(query, state, 2, user_dao)


@create_router.callback_query(SelectTestTypeCallback.filter(F.type_ == "nkt"))
async def create_grant_nkt_select(query, state: FSMContext, user_dao: UserDAO):
    await set_type(query, state, 3, user_dao)


async def create_grant(msg, state, user_dao: UserDAO) -> GrantDAO | None:
    data = await state.get_data()
    if not all([data.get("iin"), data.get("ikt"), data.get("year"), data.get("type")]):
        return None
    grant = Grant(
        iin=data["iin"],
        ikt=data["ikt"],
        year=int(data["year"]),
        type_=data["type"],
        user_id=user_dao.user.id,
    )
    grant_dao = GrantDAO()
    await grant_dao.create_grant(grant)
    await msg.bot.edit_message_text(
        _(Text.create_grant_success),
        chat_id=msg.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await grant_list_kb_gen(await user_dao.get_grants()),
    )
    await state.set_state(States.list_grants)
    await state.update_data(
        {
            "iin_check": False,
            "ikt_check": False,
            "year_check": False,
            "test_type_check": False,
            "type": None,
            "iin": None,
            "ikt": None,
            "year": None,
        }
    )
    return grant_dao


async def set_type(query, state: FSMContext, type_: int, user_dao: UserDAO):
    if await state.get_state() != States.create_grant.state:
        return

    await state.update_data({"test_type_check": True, "type": type_})

    if await create_grant(query.message, state, user_dao):
        return

    await query.message.bot.edit_message_text(
        _(Text.set_type_success),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await create_grant_kb_gen(state),
    )
