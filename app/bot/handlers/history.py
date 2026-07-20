from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
def get_router(service):
    router = Router()
    @router.message(Command("history"))
    async def history(message: Message):
        rows = await service.repo.get_history(message.from_user.id)
        text = "История:\n"
        for r in rows[:10]:
            text += f"{r['name']} {r['weight']}x{r['reps']}\n"
        await message.answer(text)
    return router