import asyncio
import os
from aiogram import Bot, Dispatcher
from app.db.db import create_pool
from app.repositories.workout_repo import WorkoutRepo
from app.services.workout_service import WorkoutService
from app.bot.handlers.start import get_router as start_router
from app.bot.handlers.plan import get_router as plan_router
from app.bot.handlers.workout import get_router as workout_router
async def init_db(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS workouts (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            started_at TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS exercises (
            id SERIAL PRIMARY KEY,
            name TEXT
        );
        CREATE TABLE IF NOT EXISTS workout_exercises (
            id SERIAL PRIMARY KEY,
            workout_id INT,
            exercise_id INT,
            order_index INT
        );
        CREATE TABLE IF NOT EXISTS sets (
            id SERIAL PRIMARY KEY,
            workout_exercise_id INT,
            weight FLOAT,
            reps INT
        );
        """)
        # фикс старой схемы
        await conn.execute("""
        ALTER TABLE workouts
        ADD COLUMN IF NOT EXISTS user_id BIGINT;
        """)
        await conn.execute("""
        INSERT INTO exercises (id, name)
        VALUES (1, 'Жим лёжа'), (2, 'Присед')
        ON CONFLICT (id) DO NOTHING;
        """)
async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    pool = await create_pool()
    await init_db(pool)

    repo = WorkoutRepo(pool)
    service = WorkoutService(repo)

    dp.include_router(start_router(service))
    dp.include_router(plan_router(service))
    dp.include_router(workout_router(service))

    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Bot started")
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("❌ Bot stopped")