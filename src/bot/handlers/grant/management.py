from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from src.bot.callback import GrantInfoActionCallback
from src.bot.callback import ListGrantCallback
from src.bot.keyboards.settings import grant_list_action_kb_gen
from src.bot.keyboards.settings import grant_list_kb_gen
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.GrantDAO import GrantDAO

management_router = Router(name="management")


@management_router.callback_query(ListGrantCallback.filter())
async def get_grant_info(query, callback_data: ListGrantCallback, state: FSMContext):
    grant_dao = GrantDAO()
    await grant_dao.get_grant_by_ikt(callback_data.ikt)
    grant = grant_dao.grant
    await query.message.bot.edit_message_text(
        _(Text.grant_info).format(
            iin=grant.iin,
            ikt=grant.ikt,
            year=grant.year,
            test_type=await grant_dao.get_type(),
        ),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=await grant_list_action_kb_gen(await grant_dao.get_ikt()),
    )


@management_router.callback_query(GrantInfoActionCallback.filter(F.action == "delete"))
async def delete_grant_handler(
    query, callback_data: GrantInfoActionCallback, state: FSMContext
):
    grant_dao = GrantDAO()
    await grant_dao.get_grant_by_ikt(callback_data.ikt)
    await grant_dao.delete_grant()
    await query.message.bot.edit_message_text(
        _(Text.grant_list),
        chat_id=query.message.chat.id,
        message_id=(await state.get_data())["root_message_id"],
        reply_markup=grant_list_kb_gen(
            await (await state.get_data())["user_dao"].get_grants()
        ),
    )
    await state.set_state(States.list_grants)
