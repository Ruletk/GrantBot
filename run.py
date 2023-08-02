import asyncio

from src.bot import bot
from src.bot import dp


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
