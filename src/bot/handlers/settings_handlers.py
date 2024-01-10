import asyncio

from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from src.bot.callback import CancelCallback
from src.bot.callback import SettingsCallback
from src.bot.keyboards.default import default_kb_gen
from src.bot.keyboards.language import language_kb_gen
from src.bot.keyboards.settings import delete_me_kb_gen
from src.bot.keyboards.settings import settings_kb_gen
from src.bot.states import States
from src.bot.text import Text
from src.db.dao.UserDAO import UserDAO

settings_router = Router(name="settings")


@settings_router.message(lambda msg: msg.text == __(Text.settings_btn))
async def settings_message_handler(msg: Message, state: FSMContext, user_dao: UserDAO):
    await state.set_state(States.settings)
    last_settings_message_id = (await state.get_data()).get("last_settings_message_id")
    if last_settings_message_id:
        for msg_id in last_settings_message_id:
            await msg.bot.delete_message(chat_id=msg.chat.id, message_id=msg_id)

    await state.update_data(
        {
            "root_message_id": msg.message_id + 1,
            "last_settings_message_id": [msg.message_id + 1, msg.message_id],
        }
    )

    await msg.answer(
        _(Text.settings_menu),
        reply_markup=await settings_kb_gen(await user_dao.get_user_language()),
    )


@settings_router.callback_query(CancelCallback.filter(F.cancel_type == "to_settings"))
async def create_grant_cancel_handler(query, state: FSMContext):
    await query.message.bot.edit_message_text(
        _(Text.settings_menu),
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=await settings_kb_gen(),
    )
    await state.set_state(States.settings)


@settings_router.callback_query(SettingsCallback.filter(F.action == "delete_me"))
async def delete_me(callback, callback_data: dict, state: FSMContext):
    await state.set_state(States.delete_me)
    await callback.message.bot.edit_message_text(
        _(Text.delete_ask),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await delete_me_kb_gen(),
    )


@settings_router.callback_query(SettingsCallback.filter(F.action == "delete_me_sure"))
async def confirmed_deletion(
    callback, callback_data: dict, state: FSMContext, user_dao: UserDAO
):
    await user_dao.delete_user()
    await asyncio.sleep(
        2
    )  # Pretending that we are doing something. User thinks that we are deleting him.
    await callback.message.bot.delete_message(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id
    )
    await callback.message.answer(
        _(Text.delete_success), reply_markup=await default_kb_gen()
    )
    await state.clear()


@settings_router.callback_query(SettingsCallback.filter(F.action == "change_lang"))
async def change_lang_settings(
    callback, callback_data: SettingsCallback, state: FSMContext, user_dao: UserDAO
):
    data = await state.get_data()
    lang = callback_data.lang
    if lang == "default":
        await callback.message.bot.edit_message_text(
            _(Text.language_change),
            chat_id=callback.message.chat.id,
            message_id=data.get("root_message_id"),
            reply_markup=await language_kb_gen(),
        )
        return
    await user_dao.set_lang(lang)
    await callback.message.bot.delete_message(
        chat_id=callback.message.chat.id, message_id=callback.message.message_id
    )

    await callback.message.bot.send_message(
        text=_(Text.language_change, locale=lang),
        chat_id=callback.message.chat.id,
        reply_markup=await default_kb_gen(locale=lang),
    )


@settings_router.callback_query(
    SettingsCallback.filter(
        F.action == "change_lang" and (F.lang == "ru" or F.lang == "kz")
    )
)
async def change_lang_callback(
    callback, callback_data: dict, state: FSMContext, user_dao: UserDAO
):
    await user_dao.set_lang(callback_data.get("lang"))
    await callback.message.bot.edit_message_text(
        _(Text.settings_menu),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=await settings_kb_gen(),
    )
