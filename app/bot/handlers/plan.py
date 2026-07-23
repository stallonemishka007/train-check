from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.inline import plan_kb
from app.utils.telegram import safe_edit_text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def handle_start(callback: CallbackQuery, state: FSMContext, service):
    await service.ensure_user(callback.from_user.id)
    await callback.message.edit_text(
        "ВЫБОР ПРОГРАММЫ ✅",
        reply_markup=plan_kb()
    )


def get_plan_edit_kb(user_id, plan_name, plan_exercises, all_custom):
    """Клавиатура для редактирования плана"""
    # список используемых ID упражнений
    used_ids = {ex['exercise_id'] for ex in plan_exercises}
    # список доступных упражнений для добавления
    available = [ex for ex in all_custom if ex['id'] not in used_ids]
    
    rows = []
    
    # показать текущие упражнения в плане
    if plan_exercises:
        rows.append([InlineKeyboardButton(text="📋 Текущие упражнения:", callback_data="plan_edit_view")])
        for ex in plan_exercises:
            rows.append([
                InlineKeyboardButton(text=f"• {ex['name']}", callback_data="noop"),
                InlineKeyboardButton(text="❌", callback_data=f"remove_ex:{plan_name}:{ex['exercise_id']}")
            ])
    
    # добавить упражнения
    if available:
        rows.append([InlineKeyboardButton(text="➕ Добавить упражнение:", callback_data="plan_edit_add")])
        for ex in available:
            rows.append([InlineKeyboardButton(text=f"+ {ex['name']}", callback_data=f"add_ex:{plan_name}:{ex['id']}")])
    
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="start")])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_router(service):
    router = Router()

    @router.callback_query(lambda c: c.data == "start")
    async def choose_plan(callback: CallbackQuery, state: FSMContext):
        await handle_start(callback, state, service)
        await callback.answer()

    @router.callback_query(lambda c: c.data == "plan:custom")
    async def select_custom_plan(callback: CallbackQuery, state: FSMContext):
        await service.set_plan(callback.from_user.id, "custom")
        ex = await service.start_workout(callback.from_user.id)
        from app.bot.keyboards.inline import session_kb
        weight = service.sessions[callback.from_user.id]["current_weight"]
        fmt_str = f"{ex['name']}\n{ex['done']}/{ex['sets']}\nТекущий вес: {weight} kg"
        await safe_edit_text(callback, fmt_str, reply_markup=session_kb(weight))
        from app.bot.states.workout import WorkoutState
        await state.set_state(WorkoutState.waiting_input)
        await callback.answer()

    @router.callback_query(lambda c: c.data.startswith("edit_plan:"))
    async def edit_plan(callback: CallbackQuery, state: FSMContext):
        plan_name = callback.data.split(":")[1]
        all_custom = await service.get_custom_exercises(callback.from_user.id)
        plan_exercises = await service.get_plan_exercises(callback.from_user.id, plan_name)
        
        if not all_custom:
            await safe_edit_text(
                callback,
                "У вас нет кастомных упражнений для редактирования плана.\nСначала создайте упражнения в разделе 'Мои упражнения'",
                reply_markup=plan_kb()
            )
        else:
            kb = get_plan_edit_kb(callback.from_user.id, plan_name, plan_exercises, all_custom)
            await safe_edit_text(
                callback,
                f"Редактирование программы '{plan_name}'",
                reply_markup=kb
            )
        await callback.answer()

    @router.callback_query(lambda c: c.data.startswith("add_ex:"))
    async def add_exercise_to_plan(callback: CallbackQuery):
        parts = callback.data.split(":")
        plan_name = parts[1]
        exercise_id = int(parts[2])
        
        # получить текущее количество упражнений в плане
        plan_exercises = await service.get_plan_exercises(callback.from_user.id, plan_name)
        order_index = len(plan_exercises)
        
        await service.add_exercise_to_plan(callback.from_user.id, plan_name, exercise_id, order_index)
        
        # перезагрузить клавиатуру
        all_custom = await service.get_custom_exercises(callback.from_user.id)
        plan_exercises = await service.get_plan_exercises(callback.from_user.id, plan_name)
        kb = get_plan_edit_kb(callback.from_user.id, plan_name, plan_exercises, all_custom)
        await safe_edit_text(callback, f"Редактирование программы '{plan_name}'", reply_markup=kb)
        await callback.answer()

    @router.callback_query(lambda c: c.data.startswith("remove_ex:"))
    async def remove_exercise_from_plan(callback: CallbackQuery):
        parts = callback.data.split(":")
        plan_name = parts[1]
        exercise_id = int(parts[2])
        
        await service.remove_exercise_from_plan(callback.from_user.id, plan_name, exercise_id)
        
        # перезагрузить клавиатуру
        all_custom = await service.get_custom_exercises(callback.from_user.id)
        plan_exercises = await service.get_plan_exercises(callback.from_user.id, plan_name)
        kb = get_plan_edit_kb(callback.from_user.id, plan_name, plan_exercises, all_custom)
        await safe_edit_text(callback, f"Редактирование программы '{plan_name}'", reply_markup=kb)
        await callback.answer()

    @router.callback_query(lambda c: c.data == "noop")
    async def noop(callback: CallbackQuery):
        await callback.answer()

    return router