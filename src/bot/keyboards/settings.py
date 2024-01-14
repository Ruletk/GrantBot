from typing import List

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from src.bot.callback import CancelCallback
from src.bot.callback import CreateGrantCallback
from src.bot.callback import GrantInfoActionCallback
from src.bot.callback import ListGrantCallback
from src.bot.callback import SelectTestTypeCallback
from src.bot.callback import SettingsCallback
from src.bot.text import Text
from src.db.models.Grant import Grant


async def settings_kb_gen(locale=None):
    create_grant = InlineKeyboardButton(
        text=_(Text.add_grant),
        callback_data=SettingsCallback(action="create_grant").pack(),
    )
    list_grant = InlineKeyboardButton(
        text=_(Text.list_grants),
        callback_data=SettingsCallback(action="list_grants").pack(),
    )
    change_lang = InlineKeyboardButton(
        text=_(Text.set_change_lang_btn),
        callback_data=SettingsCallback(action="change_lang").pack(),
    )
    delete_me = InlineKeyboardButton(
        text=_(Text.delete_me_btn),
        callback_data=SettingsCallback(action="delete_me").pack(),
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[[create_grant, list_grant], [change_lang], [delete_me]],
    )


async def delete_me_kb_gen():
    sure = InlineKeyboardButton(
        text=_(Text.confirm_deletion_btn),
        callback_data=SettingsCallback(action="delete_me_sure").pack(),
    )
    back = InlineKeyboardButton(
        text=_(Text.back),
        callback_data=CancelCallback(cancel_type="to_settings").pack(),
    )
    return InlineKeyboardMarkup(inline_keyboard=[[sure], [back]])


async def create_grant_kb_gen(state: FSMContext):
    data = await state.get_data()
    iin_check = data.get("iin_check", False)
    ikt_check = data.get("ikt_check", False)
    year_check = data.get("year_check", False)
    test_type_check = data.get("test_type_check", False)

    def checked(text, check):
        if check:
            return f"✅ {text}"
        return f"❌ {text}"

    iin = InlineKeyboardButton(
        text=checked(_(Text.iin), iin_check),
        callback_data=CreateGrantCallback(type_="iin").pack(),
    )
    ikt = InlineKeyboardButton(
        text=checked(_(Text.ikt), ikt_check),
        callback_data=CreateGrantCallback(type_="ikt").pack(),
    )
    year = InlineKeyboardButton(
        text=checked(_(Text.year), year_check),
        callback_data=CreateGrantCallback(type_="year").pack(),
    )
    test_type = InlineKeyboardButton(
        text=checked(_(Text.set_type_btn), test_type_check),
        callback_data=CreateGrantCallback(type_="test_type").pack(),
    )
    back = InlineKeyboardButton(
        text=_(Text.back),
        callback_data=CancelCallback(cancel_type="to_settings").pack(),
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[[iin], [ikt], [year], [test_type], [back]]
    )


async def create_test_type_kb_gen():
    ent = InlineKeyboardButton(
        text=_(Text.ent),
        callback_data=SelectTestTypeCallback(type_="ent").pack(),
    )
    mag = InlineKeyboardButton(
        text=_(Text.mag),
        callback_data=SelectTestTypeCallback(type_="mag").pack(),
    )
    nkt = InlineKeyboardButton(
        text=_(Text.nkt),
        callback_data=SelectTestTypeCallback(type_="nkt").pack(),
    )
    return InlineKeyboardMarkup(inline_keyboard=[[ent], [mag], [nkt]])


async def inline_cancel_kb_gen(cancel_type: str):
    cancel = InlineKeyboardButton(
        text=_(Text.cancel),
        callback_data=CancelCallback(cancel_type=cancel_type).pack(),
    )
    return InlineKeyboardMarkup(inline_keyboard=[[cancel]])


async def grant_list_kb_gen(grants: List[Grant]):
    buttons = []
    for grant in grants:
        text = _(Text.grant_info_inline).format(
            iin=grant.iin,
            ikt=grant.ikt,
            year=grant.year,
            test_type=_([Text.ent, Text.mag, Text.nkt][grant.type - 1]),
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    text=text, callback_data=ListGrantCallback(ikt=grant.ikt).pack()
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text=_(Text.back),
                callback_data=CancelCallback(cancel_type="to_settings").pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def grant_list_action_kb_gen(ikt: str):
    buttons = [
        [
            InlineKeyboardButton(
                text=_(Text.test_result_btn),
                callback_data=GrantInfoActionCallback(
                    action="get_result", ikt=ikt
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=_(Text.delete),
                callback_data=GrantInfoActionCallback(action="delete", ikt=ikt).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=_(Text.back),
                callback_data=CancelCallback(cancel_type="list_grants").pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def grant_delete_sure_kb_gen(ikt: str):
    buttons = [
        [
            InlineKeyboardButton(
                text=_(Text.yes),
                callback_data=GrantInfoActionCallback(
                    action="delete_sure", ikt=ikt
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=_(Text.back),
                callback_data=CancelCallback(cancel_type="list_grants").pack(),
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
