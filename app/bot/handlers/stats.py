from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


def get_router(service):
    router = Router()

    @router.message(Command("history"))
    async def history_cmd(message: Message):
        await service.ensure_user(message.from_user.id)
        rows = await service.get_history(message.from_user.id, limit=10)
        if not rows:
            await message.answer("История тренировок пуста")
            return
        text_lines = []
        for r in rows:
            text_lines.append(f"{r.get('started_at')} - {r.get('name')} {r.get('weight')}x{r.get('reps')}")
        await message.answer("\n".join(text_lines))

    @router.message(Command("stats"))
    async def stats_cmd(message: Message):
        await service.ensure_user(message.from_user.id)
        st = await service.get_stats(message.from_user.id)
        await message.answer(f"Тренировок: {st.get('workouts_count')}\nСетов: {st.get('sets_count')}\nСредний вес: {st.get('avg_weight')}")

    return router
