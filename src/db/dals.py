from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User


class UserDAL:
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def get_user(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = await self.session.scalar(stmt)
        return user

    async def create_user(self, telegram_id: int) -> User | None:
        try:
            user = User(telegram_id=telegram_id)
            await user.save(self.session)
        except Exception as ex:
            print(ex)
            return None

    async def update_user(self, telegram_id: int, **kwargs) -> User:
        user = await self.get_user(telegram_id)
        await user.update(self.session, **kwargs)

    async def get_result(self, telegram_id: int) -> dict:
        user = await self.get_user(telegram_id)
