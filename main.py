import asyncio
from aiogram import Bot, Dispatcher

from app.core.config import BOT_TOKEN
from app.core.db import create_pool

from app.db.repositories.workout_repo import WorkoutRepository
from app.services.workout_service import WorkoutService

from app.bot.handlers.today import get_router as today_router
from app.bot.handlers.workout import get_router as workout_router

async def main():
    # — бот —
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # --- база ---
    pool = await create_pool()
    # --- слои ---
    repo = WorkoutRepository(pool)
    service = WorkoutService(repo)
    # --- роутеры ---
    dp.include_router(today_router(service))
    dp.include_router(workout_router(service))
    # --- запуск ---
    await dp.start_polling(bot)
    if name == "main":
    asyncio.run(main())