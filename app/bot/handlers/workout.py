from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.keyboards.inline import exercise_kb, finish_kb


def get_router(service):
    router = Router()


    # --- старт тренировки ---
    @router.callback_query(F.data.startswith("ws:start:"))
    async def start_workout(callback: CallbackQuery):
        _, _, workout_id = callback.data.split(":")
        workout_id = int(workout_id)
        ex = await service.start_workout(
            callback.from_user.id,
            workout_id
        )
        await callback.message.answer(
            f"{ex['name']}\n{ex['done']}/{ex['sets']} подходов",
            reply_markup=exercise_kb(ex["id"], workout_id),
        )
        await callback.answer()


    # --- добавить подход ---
    @router.callback_query(F.data.startswith("set:add:"))
    async def add_set(callback: CallbackQuery):
        _, _, ex_id = callback.data.split(":")
        ex_id = int(ex_id)
        result = await service.add_set(callback.from_user.id, ex_id)
        await callback.message.answer(
            f"Подход добавлен ✅\n{result['done']}/{result['total']}"
        )
        await callback.answer()


    # --- следующее упражнение ---
    @router.callback_query(F.data.startswith("we:next:"))
    async def next_exercise(callback: CallbackQuery):
        _, _, workout_id = callback.data.split(":")
        workout_id = int(workout_id)
        ex = await service.next_exercise(workout_id)
        if not ex:
            await callback.message.answer(
                "Все упражнения выполнены ✅", reply_markup=finish_kb(workout_id)
            )
            await callback.answer()
            return
        await callback.message.answer(
            f"{ex['name']}\n{ex['done']}/{ex['sets']}",
            reply_markup=exercise_kb(ex["id"], workout_id),
        )
        await callback.answer()


    # --- завершение тренировки ---
    @router.callback_query(F.data.startswith("ws:finish:"))
    async def finish_workout(callback: CallbackQuery):
        _, _, workout_id = callback.data.split(":")
        workout_id = int(workout_id)
        await service.finish_workout(workout_id)
        await callback.message.answer("Тренировка завершена ✅")
        await callback.answer()


    return router
