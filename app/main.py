import os
from aiogram import Bot, Dispatcher
from app.db.db import create_pool
from app.repositories.workout_repo import WorkoutRepo
from app.services.workout_service import WorkoutService
from app.bot.handlers.workout import get_router as workout_router
from app.bot.handlers.history import get_router as history_router
async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    pool = await create_pool()
    repo = WorkoutRepo(pool)
    service = WorkoutService(repo)
    dp.include_router(workout_router(service))
    dp.include_router(history_router(service))
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())