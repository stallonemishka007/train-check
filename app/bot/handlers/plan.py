from aiogram import Router
from aiogram.types import CallbackQuery
from app.bot.keyboards.inline import plan_kb
def get_router(service):
    router = Router()
    @router.callback_query(lambda c: c.data == "start")
    async def choose_plan(callback: CallbackQuery):
        exists = await service.ensure_user(callback.from_user.id)
        if not exists:
            await callback.message.edit_text(
                "Выбери план тренировок:",
                reply_markup=plan_kb()
            )
        else:
            await callback.message.edit_text("Начинаем тренировку...")
        await callback.answer()
    return router