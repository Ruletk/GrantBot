from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.bot.callback import CancelCallback
from src.bot.keyboards.settings import grant_list_kb_gen
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.UserDAO import UserDAO

list_router = Router(name="list")


@list_router.message(F.text == __(Text.list_grants))
async def list_results(msg: Message, state: FSMContext, user_dao: UserDAO):
    grants = await user_dao.get_grants()
    if not grants:
        await msg.answer(_(Text.field_required))
        return
    await msg.answer(_(Text.grant_list), reply_markup=await grant_list_kb_gen(grants))
    await state.set_state(States.list_grants)
    await state.set_data({"root_message_id": msg.message_id + 1, "user_dao": user_dao})


@list_router.callback_query(CancelCallback.filter(F.cancel_type == "list_grants"))
async def list_grants_cancel_handler(query, state: FSMContext):
    await query.message.bot.edit_message_text(
        _(Text.grant_list),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await grant_list_kb_gen(
            await (await state.get_data())["user_dao"].get_grants()
        ),
    )
    await state.set_state(States.list_grants)
