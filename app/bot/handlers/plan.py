from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.inline import plan_kb
from app.bot.states.workout import WorkoutState
def get_router(service):
    router = Router()
    @router.callback_query(lambda c: c.data == "start")
    async def choose_plan(callback: CallbackQuery, state: FSMContext):
        exists = await service.ensure_user(callback.from_user.id)
        # ✅ ВСЕГДА показываем выбор плана
        await callback.message.edit_text(
            "Выбери план тренировок:",
            reply_markup=plan_kb()
        )
        await callback.answer()
    return router