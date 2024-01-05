import json
from time import time

from sqlalchemy import select

from src.db.models.User import User
from src.injector.injector import injector


class UserDAO:
    def __init__(self):
        self.user = None
        self.session = injector.get("session")

    async def _get_user(self, **kwargs) -> User | None:
        """Generalized method for getting user by any field."""
        async with self.session() as session:
            stmt = select(User).filter_by(**kwargs)
            res = await session.execute(stmt)
            self.user = res.scalars().first()
            return self.user

    async def _save_user(self) -> None:
        async with self.session() as session:
            session.add(self.user)
            await session.commit()

    async def _update_user(self, **kwargs) -> None:
        {setattr(self.user, key, value) for key, value in kwargs.items()}  # noqa
        await self._save_user()

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """Find user by telegram id."""
        return await self._get_user(telegram_id=telegram_id)

    async def create_user(self, telegram_id: int) -> User | None:
        self.user = User(telegram_id=telegram_id)
        await self._save_user()
        return self.user

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

    async def get_user_language(self) -> str:
        user = self.user or await self.session.get(User, self.user.id)
        return user.language or "ru"
