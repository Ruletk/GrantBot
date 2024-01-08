import logging

from sqlalchemy import select

from src.db.models.Grant import Grant
from src.db.models.User import User
from src.injector.injector import injector


logger = logging.getLogger(__name__)


class UserDAO:
    def __init__(self):
        logger.debug("Initializing")
        self.user = None
        self.session = injector.get("session")

    async def _get_user(self, **kwargs) -> User | None:
        """Generalized method for getting user by any field."""
        logger.debug("Getting user, kwargs: %s", kwargs)
        async with self.session() as session:
            stmt = select(User).filter_by(**kwargs)
            res = await session.execute(stmt)
            self.user = res.scalars().first()
            return self.user

    async def _save_user(self) -> None:
        logger.debug("Saving user")
        async with self.session() as session:
            session.add(self.user)
            await session.commit()

    async def _update_user(self, **kwargs) -> None:
        logger.debug("Updating user, kwargs: %s", kwargs)
        {setattr(self.user, key, value) for key, value in kwargs.items()}  # noqa
        await self._save_user()

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """Find user by telegram id."""
        logger.debug("Getting user by telegram id: %s", telegram_id)
        return await self._get_user(telegram_id=telegram_id)

    async def create_user(self, telegram_id: int) -> User | None:
        """Create user by telegram id."""
        logger.debug("Creating user by telegram id: %s", telegram_id)
        self.user = User(telegram_id=telegram_id)
        await self._save_user()
        return self.user

    async def get_user_language(self) -> str:
        user = self.user or await self.session.get(User, self.user.id)
        return user.language or "ru"

    async def set_lang(self, lang: str):
        logger.debug("Setting language: %s for user %s", lang, self.user)
        await self._update_user(language=lang, last_request={})

    async def delete_user(self) -> None:
        logger.debug("Deleting user: %s", self.user)
        pass

    async def confirm_policy(self) -> None:
        await self._update_user(policy_confirm=True)

    async def add_grant(self, grant: Grant):
        logger.debug("Adding grant: %s for user %s", grant, self.user)
        self.user.grants.append(grant)
        await self._save_user()

    async def remove_grant(self, grant: Grant):
        logger.debug("Removing grant: %s for user %s", grant, self.user)
        self.user.grants.remove(grant)
        await self._save_user()

    async def get_grants(self):
        logger.debug("Getting grants for user: %s", self.user)
        async with self.session() as session:
            stmt = select(Grant).filter_by(user_id=self.user.id, is_active=1)
            res = await session.execute(stmt)
            return res.scalars().all()
