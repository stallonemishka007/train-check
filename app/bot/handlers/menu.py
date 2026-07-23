from aiogram import Router
from aiogram.types import CallbackQuery
from app.bot.keyboards.inline import main_menu_kb, manage_exercises_kb
from app.utils.telegram import safe_edit_text


def get_router(service):
    router = Router()

    @router.callback_query(lambda c: c.data == "menu")
    async def show_main_menu(callback: CallbackQuery):
        await safe_edit_text(callback, "Главное меню", reply_markup=main_menu_kb())
        await callback.answer()

    @router.callback_query(lambda c: c.data == "history_btn")
    async def show_history_btn(callback: CallbackQuery):
        await service.ensure_user(callback.from_user.id)
        rows = await service.get_history(callback.from_user.id, limit=10)
        if not rows:
            await safe_edit_text(callback, "История тренировок пуста", reply_markup=main_menu_kb())
        else:
            text_lines = ["История тренировок:\n"]
            for r in rows:
                text_lines.append(f"{r.get('started_at')} - {r.get('name')} {r.get('weight')}x{r.get('reps')}")
            await safe_edit_text(callback, "\n".join(text_lines), reply_markup=main_menu_kb())
        await callback.answer()

    @router.callback_query(lambda c: c.data == "stats_btn")
    async def show_stats_btn(callback: CallbackQuery):
        await service.ensure_user(callback.from_user.id)
        st = await service.get_stats(callback.from_user.id)
        msg = f"Статистика:\n\nТренировок: {st.get('workouts_count')}\nСетов: {st.get('sets_count')}\nСредний вес: {st.get('avg_weight')}"
        await safe_edit_text(callback, msg, reply_markup=main_menu_kb())
        await callback.answer()

    @router.callback_query(lambda c: c.data == "manage_exercises")
    async def show_manage_exercises(callback: CallbackQuery):
        await safe_edit_text(callback, "Управление упражнениями", reply_markup=manage_exercises_kb())
        await callback.answer()

    return router
