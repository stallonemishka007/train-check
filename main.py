import asyncio
import os
from aiogram import Bot, Dispatcher
from app.db.db import create_pool
from app.repositories.workout_repo import WorkoutRepo
from app.services.workout_service import WorkoutService
from app.bot.handlers.start import get_router as start_router
from app.bot.handlers.plan import get_router as plan_router
from app.bot.handlers.workout import get_router as workout_router
from app.bot.handlers.schedule import get_router as schedule_router
from app.core.scheduler import scheduler as background_scheduler
from app.bot.handlers.stats import get_router as stats_router
from app.bot.handlers.menu import get_router as menu_router
from app.bot.handlers.exercises import get_router as exercises_router
async def init_db(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
        ALTER TABLE users ADD COLUMN IF NOT EXISTS plan TEXT;
        """)
        await conn.execute("""
        UPDATE users SET plan='full' WHERE plan IS NULL;
        """)
        await conn.execute("""
        DROP TABLE IF EXISTS sets CASCADE;
        DROP TABLE IF EXISTS workout_exercises CASCADE;
        DROP TABLE IF EXISTS workouts CASCADE;
        DROP TABLE IF EXISTS exercises CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        """)
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            plan TEXT,
            schedule_days TEXT,
            notify_time TIME,
            last_notified DATE
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
        
        CREATE TABLE IF NOT EXISTS user_exercise_meta (
            user_id BIGINT,
            exercise_id INT,
            last_weight FLOAT,
            PRIMARY KEY (user_id, exercise_id)
        );

        CREATE TABLE IF NOT EXISTS custom_exercises (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            name TEXT,
            default_weight FLOAT,
            default_reps INT,
            default_sets INT,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS plan_exercises (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            plan_name TEXT,
            exercise_id INT,
            order_index INT,
            FOREIGN KEY (exercise_id) REFERENCES custom_exercises(id) ON DELETE CASCADE
        );
        """)
        await conn.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS plan TEXT;
        """)
        await conn.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS schedule_days TEXT;
        """)
        await conn.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS notify_time TIME;
        """)
        await conn.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS last_notified DATE;
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
    dp.include_router(schedule_router(service))
    dp.include_router(stats_router(service))
    dp.include_router(menu_router(service))
    dp.include_router(exercises_router(service))

    # запустить планировщик уведомлений
    asyncio.create_task(background_scheduler(bot, repo))

    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Bot started")
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("❌ Bot stopped")