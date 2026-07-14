from aiogram import Router, F
from aiogram.types import CallbackQuery
def get_router(workout_service):
    router = Router()
    @router.callback_query(F.data.startswith("set_"))
    async def add_set(callback: CallbackQuery):
        workout_id, ex_index = map(int, callback.data.split("_")[1:])
        status = await workout_service.add_set(workout_id, ex_index)
        await callback.message.answer(f"✅ Подход добавлен. Статус: {status}")
        await callback.answer()
    return router