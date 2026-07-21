import re
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.bot.states.workout import WorkoutState
from app.bot.keyboards.inline import exercise_kb
def get_router(service):
    router = Router()
    def fmt(ex):
        return f"{ex['name']}\n{ex['done']}/{ex['sets']}"
    @router.callback_query(lambda c: c.data.startswith("plan:"))
    async def start_workout(callback: CallbackQuery, state: FSMContext):
        ex = await service.start_workout(callback.from_user.id)
        await callback.message.edit_text(fmt(ex) + "\n\nВведи 80x8",
                                         reply_markup=exercise_kb(ex["id"]))
        await state.set_state(WorkoutState.waiting_input)
        await callback.answer()
    @router.callback_query(lambda c: c.data.startswith("set:"))
    async def next_set(callback: CallbackQuery):
        await callback.message.answer("Введи 80x8")
        await callback.answer()
    @router.message(WorkoutState.waiting_input)
    async def input_handler(message: Message, state: FSMContext):
        m = re.match(r"(\d+(\.\d+)?)x(\d+)", message.text.replace(" ", ""))
        if not m:
            await message.answer("Формат: 80x8")
            return
        weight = float(m.group(1))
        reps = int(m.group(3))
        result = await service.add_set(message.from_user.id, weight, reps)
        if result.get("status") == "finished":
            await message.answer("Тренировка завершена ✅")
            await state.clear()
        else:
            await message.answer(fmt(result), reply_markup=exercise_kb(result["id"]))
    return router