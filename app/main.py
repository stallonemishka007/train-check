import asyncio
import os
from aiogram import Bot, Dispatcher
from app.db.db import create_pool
from app.repositories.workout_repo import WorkoutRepo
from app.services.workout_service import WorkoutService
from app.bot.handlers.start import get_router as start_router
from app.bot.handlers.plan import get_router as plan_router
from app.bot.handlers.workout import get_router as workout_router
async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    # ✅ подключение к БД
    pool = await create_pool()
    repo = WorkoutRepo(pool)
    service = WorkoutService(repo)
    # ✅ подключение роутеров
    dp.include_router(start_router(service))
    dp.include_router(plan_router(service))
    dp.include_router(workout_router(service))
    print("✅ Bot started")
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("❌ Bot stopped")