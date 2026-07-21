from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.inline import plan_kb


async def handle_start(callback: CallbackQuery, state: FSMContext, service):
    await service.ensure_user(callback.from_user.id)
    await callback.message.edit_text(
        "Выбери план тренировок:",
        reply_markup=plan_kb()
    )


def get_router(service):
    router = Router()

    @router.callback_query(lambda c: c.data == "start")
    async def choose_plan(callback: CallbackQuery, state: FSMContext):
        await handle_start(callback, state, service)
        await callback.answer()

    return router