import logging
from abc import ABC
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Coroutine
from typing import Dict
from typing import Optional
from typing import Set

from aiogram import BaseMiddleware as AbstractBaseMiddleware
from aiogram import Router
from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import I18nMiddleware

from src.api.requester import Api
from src.db.dao.UserDAO import UserDAO

logger = logging.getLogger(__name__)


class BaseMiddleware(AbstractBaseMiddleware, ABC):
    def setup(
        self: AbstractBaseMiddleware, router: Router, exclude: Optional[Set[str]] = None
    ) -> AbstractBaseMiddleware:
        """Register middleware for all events in the Router"""
        if exclude is None:
            exclude = set()
        exclude_events = {"update", *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self


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


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        data = await self._provide_user(data.get("event_from_user").id, data)

        res = await handler(event, data)

        return res

    async def _provide_user(self, user_id: int, data: dict) -> dict:
        """Provide user from database.
        Get user from DB by telegram_id.
        If user not found, create new user.

        Then provide UserDAO instance."""
        logger.debug("Providing user")
        user_dao = UserDAO()
        user = await user_dao.get_user_by_telegram_id(user_id)

        if user is None:
            await user_dao.create_user(user_id)

        data["user_dao"] = user_dao

        return data


class CustomI18NMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        if "user_dao" not in data:
            raise RuntimeError("UserDAO not found in data")
        lang = await data["user_dao"].get_user_language()
        return lang
