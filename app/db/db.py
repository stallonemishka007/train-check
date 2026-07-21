import os
import asyncpg
async def create_pool():
    return await asyncpg.create_pool(
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        database=os.getenv("PGDATABASE"),
        host=os.getenv("PGHOST"),
        port=int(os.getenv("PGPORT", 5432))
    )