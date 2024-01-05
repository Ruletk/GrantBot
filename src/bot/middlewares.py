from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Coroutine
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import I18nMiddleware

from src.api.requester import Api
from src.db.dao.UserDAO import UserDAO


class ResourceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        resources = await self._provide_resources()
        data.update(resources)

        result = await handler(event, data)

        await self._cleanup(data)
        return result

    @staticmethod
    async def _provide_api_client() -> Api:
        client = Api()
        return client

    async def _provide_resources(self) -> dict:
        api_client = await self._provide_api_client()

        resources = {"api": api_client}
        return resources

    async def _cleanup(self, data: dict):
        if "api" in data:
            api: Api = data["api"]
            await api.close_session()


class UserMiddlwware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        data = await self._provide_user(data.get("event_from_user").id, data)

        res = await handler(event, data)

        return res

    async def _provide_user(self, user_id: int, data: dict):
        user_dal = UserDAO()
        user = await user_dal.get_user_by_telegram_id(user_id)

        if user is None:
            await user_dal.create_user(user_id)

        data["user_dal"] = user_dal

        return data


class CustomI18NMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        if "user_dal" not in data:
            raise RuntimeError("UserDAL not found.")
        lang = await data["user_dal"].get_user_language()
        return lang
