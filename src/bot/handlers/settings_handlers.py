from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.api.requester import Api
from src.bot.keyboards.default import ru_default_kb
from src.bot.keyboards.settings import ru_settings_kb
from src.bot.keyboards.settings import ru_type_kb
from src.bot.messages import messages
from src.bot.states import States
from src.db.dals import UserDAL
from src.db.models import User


def register_settings_handlers(dp: Dispatcher):
    @dp.message_handler(lambda msg: msg.text == "Отмена", state="*")
    async def cancel(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        await state.reset_state()
        await msg.answer(messages["ru_reset_state"], reply_markup=ru_default_kb)

    @dp.message_handler(lambda msg: msg.text == "Назад", state="*")
    async def back(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        await state.reset_state()
        await msg.answer(messages["ru_back"], reply_markup=ru_settings_kb)

    @dp.message_handler(lambda msg: msg.text == "Указать тип теста")
    async def set_type(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        await States.set_type.set()
        await msg.answer(messages["ru_set_type"], reply_markup=ru_type_kb)

    @dp.message_handler(state=States.set_type)
    async def set_type_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        if msg.text.strip() not in ["ЕНТ/КТ", "Магистратура/Докторантура", "НКТ"]:
            await msg.answer(
                messages["ru_set_type_error_by_user"], reply_markup=ru_type_kb
            )
            return
        if msg.text.strip() == "ЕНТ/КТ":
            tp = 1
        elif msg.text.strip() == "Магистратура/Докторантура":
            tp = 2
        else:
            tp = 3
        await user_dal.update_user(msg.from_user.id, user=user, type=tp)
        await msg.answer(messages["ru_set_type_success"], reply_markup=ru_settings_kb)
        await state.reset_state()

    @dp.message_handler(lambda msg: msg.text == "Указать год")
    async def set_year(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        await States.set_year.set()
        await msg.answer(messages["ru_set_year"])

    @dp.message_handler(state=States.set_year)
    async def set_year_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        try:
            value = int(msg.text.strip())
        except ValueError:
            msg.answer(messages["ru_set_year_error_by_user"])
        else:
            await user_dal.update_user(msg.from_user.id, user=user, year=value)
            await msg.answer(
                messages["ru_set_year_success"], reply_markup=ru_settings_kb
            )
            await state.reset_state()

    @dp.message_handler(lambda msg: msg.text == "Указать ИИН")
    async def set_iin(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        await States.set_iin.set()
        await msg.answer(messages["ru_set_iin"])

    @dp.message_handler(state=States.set_iin)
    async def set_iin_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        try:
            iin = msg.text.strip()
            assert len(iin) == 12
        except AssertionError:
            await msg.answer(messages["ru_iin_error_by_user"])
        else:
            await user_dal.update_user(msg.from_user.id, user, iin=iin)
            await msg.answer(
                messages["ru_set_iin_success"], reply_markup=ru_settings_kb
            )
            await state.reset_state()

    @dp.message_handler(lambda msg: msg.text == "Указать ИКТ")
    async def set_ikt(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        await States.set_ikt.set()
        await msg.answer(messages["ru_set_ikt"])

    @dp.message_handler(state=States.set_ikt)
    async def set_ikt_handler(
        msg: Message, user: User, user_dal: UserDAL, api: Api, state: FSMContext
    ):
        try:
            ikt = msg.text.strip()
            assert len(ikt) == 9
        except AssertionError:
            await msg.answer(messages["ru_ikt_error_by_user"])
        else:
            await user_dal.update_user(msg.from_user.id, user, ikt=ikt)
            await msg.answer(
                messages["ru_set_ikt_success"], reply_markup=ru_settings_kb
            )
            await state.reset_state()
