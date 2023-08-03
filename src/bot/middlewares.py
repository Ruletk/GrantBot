from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Coroutine
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import I18nMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.requester import Api
from src.db.dals import UserDAL
from src.db.engine import engine


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

    @staticmethod
    async def _provide_db_session() -> AsyncSession:
        session = AsyncSession(engine)
        return session

    async def _provide_resources(self) -> dict:
        api_client = await self._provide_api_client()
        db_session = await self._provide_db_session()

        resources = {"api": api_client, "db_session": db_session}
        return resources

    async def _cleanup(self, data: dict):
        if "db_session" in data:
            session: AsyncSession = data["db_session"]
            await session.commit()
            await session.close()

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
        if "db_session" not in data:
            raise RuntimeError("AsyncSession not found.")

        if "api" not in data:
            raise RuntimeError("RTSU API client not found.")

        db_session: AsyncSession = data.get("db_session")
        api: Api = data.get("api")

        user_dal = UserDAL(db_session)
        user = await user_dal.get_user(user_id)

        if user is None:
            await user_dal.create_user(user_id)

        data["user_dal"] = user_dal
        data["api"] = api

        return data


class CustomI18NMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user = data.get("user_dal").user
        lang = getattr(user, "language", "ru")
        return lang
