import asyncio
from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.core.db import create_pool

from app.db.repositories.workout_repo import WorkoutRepository
from app.services.workout_service import WorkoutService

from app.bot.handlers.today import get_router as today_router
from app.bot.handlers.workout import get_router as workout_router


async def main():
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()
pool = await create_pool()
repo = WorkoutRepository(pool)
service = WorkoutService(repo)
dp.include_router(today_router(service))
dp.include_router(workout_router(service))
await dp.start_polling(bot)
if __name__ == "__main__":
        asyncio.run(main())
