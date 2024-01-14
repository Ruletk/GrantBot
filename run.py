import asyncio

import src.settings  # noqa
from src.bot import bot
from src.bot import dp
from src.db.engine import initialize
from src.injector.injector import injector  # noqa


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def start_app():
    initialize()
    asyncio.run(main())


if __name__ == "__main__":
    start_app()
