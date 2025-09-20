import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from db import init_db, populate_test_data
from handlers.welcome import welcome_router
from handlers.seeker import seeker_router
from handlers.employer import employer_router

logging.basicConfig(level=logging.INFO)

async def main():
    init_db()
    populate_test_data()  # Заполняем базу данных тестовыми данными

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(welcome_router)
    dp.include_router(seeker_router)
    dp.include_router(employer_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
