import os
import asyncpg
async def create_pool():
    dsn = os.getenv("DATABASE_URL")
    print("DATABASE_URL:", dsn)  # временно для дебага
    return await asyncpg.create_pool(dsn=dsn)