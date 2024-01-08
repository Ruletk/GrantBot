from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.bot.callback import CancelCallback
from src.bot.callback import CreateGrantCallback
from src.bot.callback import SelectTestTypeCallback
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


@create_router.message(F.text == __(Text.add_grant))
async def create_result(msg: Message, state: FSMContext, user_dao: UserDAO):
    if len(await user_dao.get_grants()) >= 2:
        await msg.answer(_(Text.grants_limit))
        return
    await state.set_state(States.create_grant)

    await msg.answer(
        _(Text.create_grant), reply_markup=await create_grant_kb_gen(state)
    )
    await state.set_data(
        {"user_dao": user_dao, "grant": Grant(), "root_message_id": msg.message_id + 1}
    )


@create_router.callback_query(CancelCallback.filter(F.cancel_type == "create_grant"))
async def create_grant_cancel_handler(query, state: FSMContext):
    user_dao = (await state.get_data())["user_dao"]
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
        reply_markup=create_test_type_kb_gen(),
    )


@create_router.message(States.set_iin)
async def create_grant_set_iin(msg: Message, state: FSMContext, user_dao: UserDAO):
    iin = msg.text.strip()
    await msg.delete()

    root_message_id = (await state.get_data())["root_message_id"]
    if not validate_iin(iin):
        await msg.bot.edit_message_text(
            _(Text.set_iin_error_by_user),
            chat_id=msg.chat.id,
            message_id=root_message_id,
            reply_markup=await inline_cancel_kb_gen("create_grant"),
        )
        return
    grant = (await state.get_data())["grant"]
    grant.iin = iin

    if await create_grant(grant, msg, state):
        return

    await state.update_data({"grant": grant, "iin_check": True})
    await msg.bot.edit_message_text(
        _(Text.set_iin_success),
        chat_id=msg.chat.id,
        message_id=root_message_id,
        reply_markup=await create_grant_kb_gen(state),
    )
    await state.set_state(States.create_grant)


@create_router.message(States.set_ikt)
async def create_grant_set_ikt(msg: Message, state: FSMContext):
    await msg.delete()
    ikt = msg.text.strip()
    if not validate_ikt(ikt):
        await msg.bot.edit_message_text(
            _(Text.set_ikt_error_by_user),
            chat_id=msg.chat.id,
            message_id=(await state.get_data())["root_message_id"],
            reply_markup=await inline_cancel_kb_gen("create_grant"),
        )
        return
    grant = (await state.get_data())["grant"]
    grant.ikt = ikt

    if await create_grant(grant, msg, state):
        return

    await state.update_data({"grant": grant, "ikt_check": True})
    await msg.bot.edit_message_text(
        _(Text.set_ikt_success),
        chat_id=msg.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await create_grant_kb_gen(state),
    )
    await state.set_state(States.create_grant)


@create_router.message(States.set_year)
async def create_grant_set_year(msg: Message, state: FSMContext, user_dao: UserDAO):
    await msg.delete()
    year = msg.text.strip()
    if not validate_year(year):
        await msg.bot.edit_message_text(
            _(Text.set_year_error_by_user),
            chat_id=msg.chat.id,
            message_id=(await state.get_data())["root_message_id"],
            reply_markup=await inline_cancel_kb_gen("create_grant"),
        )
        return
    grant = (await state.get_data())["grant"]
    grant.year = int(year)
    grant.user_id = user_dao.user.id

    if await create_grant(grant, msg, state):
        return

    await state.update_data({"grant": grant, "year_check": True})
    await msg.bot.edit_message_text(
        _(Text.set_year_success),
        chat_id=msg.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await create_grant_kb_gen(state),
    )
    await state.set_state(States.create_grant)


@create_router.callback_query(SelectTestTypeCallback.filter(F.type_ == "ent"))
async def create_grant_ent_select(query, state: FSMContext):
    await set_type(query, state, 1)


@create_router.callback_query(SelectTestTypeCallback.filter(F.type_ == "mag"))
async def create_grant_mag_select(query, state: FSMContext):
    await set_type(query, state, 2)


@create_router.callback_query(SelectTestTypeCallback.filter(F.type_ == "nkt"))
async def create_grant_nkt_select(query, state: FSMContext):
    await set_type(query, state, 3)


async def create_grant(grant: Grant, msg, state) -> GrantDAO | None:
    if not all([grant.iin, grant.ikt, grant.year, grant.type]):
        return None
    grant_dao = GrantDAO()
    await grant_dao.create_grant(grant)
    await msg.bot.edit_message_text(
        _(Text.create_grant_success),
        chat_id=msg.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await grant_list_kb_gen(
            await ((await state.get_data())["user_dao"].get_grants())
        ),
    )
    await state.set_state(States.list_grants)
    return grant_dao


async def set_type(query, state: FSMContext, type_: int):
    if await state.get_state() != States.create_grant.state:
        return
    grant = (await state.get_data())["grant"]
    grant.type = type_

    grant_dao = await create_grant(grant, query.message, state)
    if grant_dao:
        await query.message.answer(_(Text.create_grant_success))
        await state.clear()
        return

    await state.update_data({"test_type_check": True, "grant": grant})

    await query.message.bot.edit_message_text(
        _(Text.set_type_success),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await create_grant_kb_gen(state),
    )
