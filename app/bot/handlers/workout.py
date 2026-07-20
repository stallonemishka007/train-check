from aiogram import Router
from aiogram.types import CallbackQuery
from app.keyboards.inline import exercise_kb
def format_text(ex):
    return (
        f"Упражнение {ex['index']}/{ex['total_exercises']}\n"
        f"{ex['name']}\n"
        f"{ex['done']}/{ex['sets']} подходов"
    )
def get_router(service):
    router = Router()
    @router.callback_query(lambda c: c.data.startswith("start:"))
    async def start_workout(callback: CallbackQuery):
        workout_id = int(callback.data.split(":")[1])
        ex = await service.start_workout(
            callback.from_user.id,
            workout_id
        )
        await callback.message.edit_text(
            format_text(ex),
            reply_markup=exercise_kb(ex["id"])
        )
        await callback.answer()
    @router.callback_query(lambda c: c.data.startswith("set:"))
    async def add_set(callback: CallbackQuery):
        ex_id = int(callback.data.split(":")[1])
        result = await service.add_set(
            callback.from_user.id,
            ex_id
        )
        if result.get("status") == "finished":
            await callback.message.edit_text(
                "Тренировка завершена ✅"
            )
        else:
            await callback.message.edit_text(
                format_text(result),
                reply_markup=exercise_kb(result["id"])
            )
        await callback.answer()
    return router