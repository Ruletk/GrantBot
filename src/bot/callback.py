from aiogram.filters.callback_data import CallbackData


class SettingsCallback(CallbackData, prefix="settings"):
    action: str
    lang: str = "default"


class CreateGrantCallback(CallbackData, prefix="create_grant"):
    type_: str


class SelectTestTypeCallback(CallbackData, prefix="select_test_type"):
    type_: str


class CancelCallback(CallbackData, prefix="cancel"):
    cancel_type: str


class ListGrantCallback(CallbackData, prefix="list_grant"):
    ikt: str


class GrantInfoActionCallback(CallbackData, prefix="grant_info_action"):
    action: str
    ikt: str
