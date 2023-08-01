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
        await user.update(self.session, **kwargs)
