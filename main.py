import asyncio as aio
import logging
from aiogram import Bot, Dispatcher

from db.database import Base, engine
from routers.router import router

TOKEN = '5311392408:AAHg8Q5VdFfgdnqhrmgNOPthjRIXUo_l3-U'  # Делаю ботю для себя, поэтому пусть токен будет открытым)


async def main():
    Base.metadata.create_all(bind=engine)
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    aio.run(main())
