from aiogram import Router
from aiogram.types import CallbackQuery
from app.bot.keyboards.inline import plan_kb
from aiogram.fsm.context import FSMContext
from app.bot.states.workout import WorkoutState
def get_router(service):
    router = Router()
    @router.callback_query(lambda c: c.data == "start")
async def choose_plan(callback: CallbackQuery, state: FSMContext):
    exists = await service.ensure_user(callback.from_user.id)
    if not exists:
        await callback.message.edit_text(
            "Выбери план тренировок:",
            reply_markup=plan_kb()
        )
    else:
        ex = await service.start_workout(callback.from_user.id)
        await callback.message.edit_text(
            f"{ex['name']}\n{ex['done']}/{ex['sets']}\n\nВведи 80x8"
        )
        await state.set_state(WorkoutState.waiting_input)
    await callback.answer()
    return router