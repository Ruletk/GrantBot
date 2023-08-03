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
        """Use user object only throught dal."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        res = await self.session.execute(stmt)
        self.user = res.scalars().first()
        return self.user

    async def create_user(self, telegram_id: int) -> User | None:
        self.user = User(telegram_id=telegram_id)
        await self.user.save(self.session)

    async def set_iin(self, iin: str):
        await self._update_user(iin=iin, last_request={})

    async def set_ikt(self, ikt: str):
        await self._update_user(ikt=ikt, last_request={})

    async def set_type(self, type: int):
        await self._update_user(type=type, last_request={})

    async def set_year(self, year: int):
        await self._update_user(year=year, last_request={})

    async def set_lang(self, lang: str):
        await self._update_user(language=lang, last_request={})

    async def _update_user(self, **kwargs) -> None:
        await self.user.update(
            self.session, updated_at=datetime.datetime.now(), **kwargs
        )

    async def delete_user(self) -> None:
        await self._update_user(
            iin=None, ikt=None, year=None, type=None, policy_confirm=False
        )

    async def get_cached(self) -> dict | None:
        if not getattr(self.user, "last_request", None):
            return None
        json_data = json.loads(self.user.last_request)
        if time() - int(json_data.get("latest_time", 0)) <= 3600:
            return json_data

    async def cache(self, data=None) -> None:
        if not data or type(data) is not dict:
            return None

        current_time = time()
        data = {"latest_time": current_time} | data
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        await self._update_user(last_request=json_data)

    async def policy_confirm(self) -> None:
        await self._update_user(policy_confirm=True)

    async def get_all_data(self) -> tuple[User.iin, User.ikt, User.type, User.year]:
        return self.user.iin, self.user.ikt, self.user.type, self.user.year
