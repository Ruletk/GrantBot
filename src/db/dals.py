import datetime
import json
from time import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User


class UserDAL:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_user(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def create_user(self, telegram_id: int) -> User | None:
        user = User(telegram_id=telegram_id)
        await user.save(self.session)

    async def update_user(self, telegram_id: int, user=None, **kwargs) -> User:
        if not user:
            user = await self.get_user(telegram_id)
        await user.update(
            self.session, updated_at=datetime.datetime.now(), last_request={}, **kwargs
        )

    async def delete_user(self, telegram_id: int = None, user=None) -> User:
        if not user:
            user = await self.get_user(telegram_id)
        await user.delete(self.session)

    async def get_cached(self, telegram_id: int, user=None) -> dict | None:
        if not user:
            user = await self.get_user(telegram_id)
        if not user.last_request:
            return None
        json_data = json.loads(user.last_request)
        if time() - int(json_data.get("latest_time", 0)) <= 3600:
            return json_data

    async def cache(self, telegram_id: int, user=None, data=None) -> None:
        if not user:
            user = await self.get_user(telegram_id)
        if not data or type(data) is not dict:
            return None

        current_time = time()
        data = {"latest_time": current_time} | data
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        user.last_request = json_data
        await user.save(self.session)
