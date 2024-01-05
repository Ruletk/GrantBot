import asyncio

from src.bot import bot
from src.bot import dp
from src.db.engine import initialize
from src.injector.injector import injector  # noqa


async def main():
    print(injector.__dict__)
    async with injector.get("session")() as session:
        print(session)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    initialize()
    asyncio.run(main())
