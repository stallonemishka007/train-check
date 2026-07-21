import os
import asyncpg
async def create_pool():
    return await asyncpg.create_pool(
        user=os.getenv("PGUSER"),
        dsn=os.getenv("DATABASE_URL")
    )