import asyncio


async def scheduler():
    while True:
        print("Scheduler работает")
        await asyncio.sleep(60)
