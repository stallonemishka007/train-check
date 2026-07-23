from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.bot.keyboards.inline import manage_exercises_kb, main_menu_kb


class ExerciseState(StatesGroup):
    waiting_name = State()
    waiting_weight = State()
    waiting_reps = State()
    waiting_sets = State()


def get_router(service):
    router = Router()

    @router.callback_query(lambda c: c.data == "add_exercise")
    async def add_exercise_start(callback: CallbackQuery, state: FSMContext):
        await callback.message.answer("Введи название упражнения")
        await state.set_state(ExerciseState.waiting_name)
        await callback.answer()

    @router.callback_query(lambda c: c.data == "list_exercises")
    async def list_exercises(callback: CallbackQuery):
        exercises = await service.get_custom_exercises(callback.from_user.id)
        if not exercises:
            await callback.message.edit_text("У тебя нет добавленных упражнений", reply_markup=manage_exercises_kb())
        else:
            lines = ["Твои упражнения:\n"]
            for ex in exercises:
                lines.append(f"• {ex['name']} - {ex['default_weight']}kg x{ex['default_reps']} (подходов: {ex['default_sets']})")
            await callback.message.edit_text("\n".join(lines), reply_markup=manage_exercises_kb())
        await callback.answer()

    @router.message(ExerciseState.waiting_name)
    async def name_input(message: Message, state: FSMContext):
        await state.update_data(name=message.text.strip())
        await message.answer("Введи начальный вес (кг)")
        await state.set_state(ExerciseState.waiting_weight)

    @router.message(ExerciseState.waiting_weight)
    async def weight_input(message: Message, state: FSMContext):
        try:
            weight = float(message.text.replace(',', '.'))
        except Exception:
            await message.answer("Неверный формат. Введи число, например 50 или 50.5")
            return
        await state.update_data(weight=weight)
        await message.answer("Введи количество повторов")
        await state.set_state(ExerciseState.waiting_reps)

    @router.message(ExerciseState.waiting_reps)
    async def reps_input(message: Message, state: FSMContext):
        try:
            reps = int(message.text.strip())
        except Exception:
            await message.answer("Неверный формат. Введи целое число")
            return
        await state.update_data(reps=reps)
        await message.answer("Введи количество подходов")
        await state.set_state(ExerciseState.waiting_sets)

    @router.message(ExerciseState.waiting_sets)
    async def sets_input(message: Message, state: FSMContext):
        try:
            sets = int(message.text.strip())
        except Exception:
            await message.answer("Неверный формат. Введи целое число")
            return
        data = await state.get_data()
        await service.add_custom_exercise(
            message.from_user.id,
            data['name'],
            data['weight'],
            data['reps'],
            sets
        )
        await message.answer(f"✅ Упражнение '{data['name']}' добавлено", reply_markup=manage_exercises_kb())
        await state.clear()

    return router
