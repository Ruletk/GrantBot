from typing import List

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _

from src.bot.callback import CancelCallback
from src.bot.callback import CreateGrantCallback
from src.bot.callback import GrantInfoActionCallback
from src.bot.callback import ListGrantCallback
from src.bot.callback import SelectTestTypeCallback
from src.bot.text import Text
from src.db.models.Grant import Grant


async def settings_kb_gen():
    create = KeyboardButton(text=_(Text.add_grant))
    list = KeyboardButton(text=_(Text.list_grants))
    change_lang = KeyboardButton(text=_(Text.set_change_lang_btn))
    delete_me = KeyboardButton(text=_(Text.delete_me_btn))
    cancel = KeyboardButton(text=_(Text.cancel))

    return ReplyKeyboardMarkup(
        keyboard=[[create, list], [change_lang], [delete_me], [cancel]],
        resize_keyboard=True,
    )


def cancel_kb_gen():
    back = KeyboardButton(text=_(Text.back))
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                back,
            ],
        ],
        resize_keyboard=True,
    )


def type_kb_gen():
    ent = InlineKeyboardButton(text=_(Text.set_ent_btn), callback_data="set_type_ent")
    mag = InlineKeyboardButton(text=_(Text.set_mag_btn), callback_data="set_type_mag")
    nkt = InlineKeyboardButton(text=_(Text.set_nkt_btn), callback_data="set_type_nkt")
    return InlineKeyboardMarkup(inline_keyboard=[[ent], [mag], [nkt]])


def delete_me_kb_gen():
    sure = KeyboardButton(text=_(Text.confirm_deletion_btn))
    back = KeyboardButton(text=_(Text.back))
    return ReplyKeyboardMarkup(keyboard=[[sure], [back]], resize_keyboard=True)


def grants_kb_gen(grants: List[Grant]):
    buttons = []
    for grant in grants:
        text = _(Text.grant_info).format(
            ikt=grant.iin, code=grant.ikt, result=grant.year
        )
        buttons.append(
            InlineKeyboardButton(text=text, callback_data=f"grant_{grant.ikt}")
        )
    # buttons.append(KeyboardButton(text=_(Text.back)))
    # return ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)


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
        text=checked(_(Text.set_iin_btn), iin_check),
        callback_data=CreateGrantCallback(type_="iin").pack(),
    )
    ikt = InlineKeyboardButton(
        text=checked(_(Text.set_ikt_btn), ikt_check),
        callback_data=CreateGrantCallback(type_="ikt").pack(),
    )
    year = InlineKeyboardButton(
        text=checked(_(Text.set_year_btn), year_check),
        callback_data=CreateGrantCallback(type_="year").pack(),
    )
    test_type = InlineKeyboardButton(
        text=checked(_(Text.set_type_btn), test_type_check),
        callback_data=CreateGrantCallback(type_="test_type").pack(),
    )
    back = InlineKeyboardButton(
        text=_(Text.back),
        callback_data=CancelCallback(cancel_type="create_grant").pack(),
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[[iin], [ikt], [year], [test_type], [back]]
    )


def create_test_type_kb_gen():
    ent = InlineKeyboardButton(
        text=_(Text.set_ent_btn),
        callback_data=SelectTestTypeCallback(type_="ent").pack(),
    )
    mag = InlineKeyboardButton(
        text=_(Text.set_mag_btn),
        callback_data=SelectTestTypeCallback(type_="mag").pack(),
    )
    nkt = InlineKeyboardButton(
        text=_(Text.set_nkt_btn),
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
            test_type=_(Text.ent_types[grant.type - 1]),
        )
        buttons.append(
            [
                InlineKeyboardButton(
                    text=text, callback_data=ListGrantCallback(ikt=grant.ikt).pack()
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
