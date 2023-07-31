from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.requester import Api
from src.db.dals import UserDAL
from src.db.engine import engine


class ResourceMiddleware(BaseMiddleware):
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

    async def on_pre_process_message(self, update: types.Message, data: dict):
        resources = await self._provide_resources()
        data.update(resources)
        return data

    async def on_pre_process_callback_query(
        self, query: types.CallbackQuery, data: dict
    ):
        resources = await self._provide_resources()
        data.update(resources)
        return data

    async def on_post_process_callback_query(
        self, query: types.CallbackQuery, data_from_handler: list, data: dict
    ):
        await self._cleanup()

    async def on_post_process_message(
        self, message: types.Message, data_from_handler: list, data: dict
    ):
        await self._cleanup(data)


class UserMiddlwware(BaseMiddleware):
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

        data["user"] = user
        data["user_dal"] = user_dal
        data["api"] = api

        return data

    async def on_pre_process_message(self, message: types.Message, data: dict):
        return await self._provide_user(message.from_user.id, data)

    async def on_pre_process_callback_query(
        self, query: types.CallbackQuery, data: dict
    ):
        return await self._provide_user(query.from_user.id, data)
