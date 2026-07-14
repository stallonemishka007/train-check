import asyncio
from aiogram import Bot, Dispatcher
from app.core.config import settings
from app.core.database import create_pool
from app.services.workout_service import WorkoutService
from app.db.repositories.workout_repo import WorkoutRepository
from app.bot.handlers.workout import get_router
from app.core.scheduler import scheduler
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
async def main():
    pool = await create_pool(settings.DB_URL)
    repo = WorkoutRepository(pool)
    service = WorkoutService(repo)
    dp.include_router(get_router(service))
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())