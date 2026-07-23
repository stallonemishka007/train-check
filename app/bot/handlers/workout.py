from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.bot.states.workout import WorkoutState
from app.bot.keyboards.inline import session_kb
from app.utils.telegram import safe_edit_text


def get_router(service):
    router = Router()

    def fmt(ex, weight):
        return f"{ex['name']}\n{ex['done']}/{ex['sets']}\nТекущий вес: {weight} kg"

    @router.callback_query(lambda c: c.data.startswith("plan:"))
    async def select_plan(callback: CallbackQuery, state: FSMContext):
        plan = callback.data.split(":")[1]
        await service.set_plan(callback.from_user.id, plan)
        ex = await service.start_workout(callback.from_user.id)
        # установить состояние ожидания и показать кнопки
        await safe_edit_text(callback, fmt(ex, service.sessions[callback.from_user.id]["current_weight"]), reply_markup=session_kb(service.sessions[callback.from_user.id]["current_weight"]))
        await state.set_state(WorkoutState.waiting_input)
        await callback.answer()

    

    @router.callback_query(lambda c: c.data.startswith("reps:"))
    async def record_set(callback: CallbackQuery, state: FSMContext):
        parts = callback.data.split(":")
        reps = parts[1]
        if reps == 'custom':
            await callback.message.answer("Введи количество повторов (число)")
            await state.set_state(WorkoutState.waiting_custom_reps)
            await callback.answer()
            return
        reps = int(reps)
        s = service.sessions.get(callback.from_user.id)
        if not s:
            await callback.answer("Сессия не найдена")
            return
        weight = s["current_weight"]
        result = await service.add_set(callback.from_user.id, weight, reps)
        if result.get("status") == "finished":
            await safe_edit_text(callback, "Тренировка завершена ✅")
            await state.clear()
            await callback.answer()
            return
        # иначе обновляем сообщение на следующий сет/упражнение
        await safe_edit_text(callback, fmt(result, s["current_weight"]), reply_markup=session_kb(s["current_weight"]))
        await callback.answer()

    @router.callback_query(lambda c: c.data == "skip")
    async def skip_exercise(callback: CallbackQuery, state: FSMContext):
        s = service.sessions.get(callback.from_user.id)
        if not s:
            await callback.answer("Сессия не найдена")
            return
        # пометить упражнение как выполненное
        s["exercises"][s["current"]]["done"] = s["exercises"][s["current"]]["sets"]
        s["current"] += 1
        if s["current"] >= len(s["exercises"]):
            await safe_edit_text(callback, "Тренировка завершена ✅")
            await state.clear()
            await callback.answer()
            return
        ex = service._current(callback.from_user.id)
        await safe_edit_text(callback, fmt(ex, s["current_weight"]), reply_markup=session_kb(s["current_weight"]))
        await callback.answer()

    @router.callback_query(lambda c: c.data.startswith("weight:"))
    async def handle_weight(callback: CallbackQuery, state: FSMContext):
        data = callback.data.split(":")[1]
        if data == 'custom':
            await callback.message.answer("Введи вес в формате 80.5 или 80")
            await state.set_state(WorkoutState.waiting_custom_weight)
            await callback.answer()
            return
        try:
            delta = int(data)
        except ValueError:
            await callback.answer()
            return
        s = service.sessions.get(callback.from_user.id)
        if not s:
            await callback.answer("Сессия не найдена")
            return
        s["current_weight"] = max(0, s["current_weight"] + delta)
        ex = service._current(callback.from_user.id)
        await safe_edit_text(callback, fmt(ex, s["current_weight"]), reply_markup=session_kb(s["current_weight"]))
        await callback.answer()

    @router.message(WorkoutState.waiting_custom_weight)
    async def custom_weight_input(message: Message, state: FSMContext):
        try:
            w = float(message.text.replace(',', '.'))
        except Exception:
            await message.answer("Неверный формат. Введи число, например 80 или 80.5")
            return
        s = service.sessions.get(message.from_user.id)
        if not s:
            await message.answer("Сессия не найдена")
            await state.clear()
            return
        s["current_weight"] = w
        ex = service._current(message.from_user.id)
        await message.answer(fmt(ex, s["current_weight"]), reply_markup=session_kb(s["current_weight"]))
        await state.clear()

    @router.message(WorkoutState.waiting_custom_reps)
    async def custom_reps_input(message: Message, state: FSMContext):
        try:
            reps = int(message.text.strip())
        except Exception:
            await message.answer("Неверный формат. Введи целое число повторов")
            return
        s = service.sessions.get(message.from_user.id)
        if not s:
            await message.answer("Сессия не найдена")
            await state.clear()
            return
        weight = s["current_weight"]
        result = await service.add_set(message.from_user.id, weight, reps)
        if result.get("status") == "finished":
            await message.answer("Тренировка завершена ✅")
            await state.clear()
            return
        await message.answer(fmt(result, s["current_weight"]), reply_markup=session_kb(s["current_weight"]))
        await state.clear()

    return router