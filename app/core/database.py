import asyncpg
async def create_pool(db_url):
    return await asyncpg.create_pool(db_url)