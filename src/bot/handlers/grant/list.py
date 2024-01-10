from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from src.bot.callback import CancelCallback
from src.bot.callback import SettingsCallback
from src.bot.keyboards.settings import grant_list_kb_gen
from src.bot.keyboards.settings import settings_kb_gen
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.UserDAO import UserDAO

list_router = Router(name="list")


@list_router.callback_query(SettingsCallback.filter(F.action == "list_grants"))
async def list_results(callback, state: FSMContext, user_dao: UserDAO):
    grants = await user_dao.get_grants()
    if not grants:
        await callback.message.bot.edit_message_text(
            _(Text.field_required),
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            reply_markup=await settings_kb_gen(),
        )
        return

    await callback.message.bot.edit_message_text(
        _(Text.grant_list),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await grant_list_kb_gen(grants),
    )
    await state.set_state(States.list_grants)


@list_router.callback_query(CancelCallback.filter(F.cancel_type == "list_grants"))
async def list_grants_cancel_handler(query, state: FSMContext, user_dao: UserDAO):
    await query.message.bot.edit_message_text(
        _(Text.grant_list),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await grant_list_kb_gen(await user_dao.get_grants()),
    )
    await state.set_state(States.list_grants)
