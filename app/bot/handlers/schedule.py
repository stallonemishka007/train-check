from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from app.bot.keyboards.inline import schedule_kb
from app.bot.states.workout import ScheduleState


def get_router(service):
    router = Router()

    @router.callback_query(lambda c: c.data == "schedule")
    async def show_schedule(callback: CallbackQuery):
        # пока показываем текущые значения из БД (упрощенно берем дефолт)
        await service.ensure_user(callback.from_user.id)
        # load current schedule
        cur = await service.get_schedule(callback.from_user.id)
        if cur:
            days = cur.get("days")
            if isinstance(days, str):
                days_list = [d.strip() for d in days.split(',') if d.strip()]
            else:
                days_list = cur.get("days") or ["Mon", "Wed", "Fri"]
            time = cur.get("time") or "17:00"
        else:
            days_list = ["Mon", "Wed", "Fri"]
            time = "17:00"
        service.start_schedule_edit(callback.from_user.id, {"days": days_list, "time": time})
        await callback.message.edit_text("Настройки расписания", reply_markup=schedule_kb(days_list, time))
        await callback.answer()

    @router.callback_query(lambda c: c.data.startswith("sched:"))
    async def schedule_action(callback: CallbackQuery, state: FSMContext):
        parts = callback.data.split(":")
        action = parts[1]
        if action == "toggle":
            day = parts[2]
            s = service.toggle_edit_day(callback.from_user.id, day)
            await callback.message.edit_text("Настройки расписания", reply_markup=schedule_kb(s.get("days"), s.get("time")))
            await callback.answer()
            return
        if action == "time":
            await callback.message.answer("Введи время уведомления в формате HH:MM")
            await state.set_state(ScheduleState.waiting_time_input)
            await callback.answer()
            return
        if action == "save":
            s = service.schedule_edits.get(callback.from_user.id)
            if not s:
                await callback.answer()
                return
            # validate time before saving
            if not service.validate_time(s.get("time", "")):
                await callback.message.answer("Неверный формат времени. Введи HH:MM")
                await state.set_state(ScheduleState.waiting_time_input)
                await callback.answer()
                return
            ok = await service.save_schedule_edit(callback.from_user.id)
            if ok:
                await callback.message.edit_text("Расписание сохранено")
            else:
                await callback.message.edit_text("Не удалось сохранить расписание")
            await callback.answer()
            return
        await callback.answer()

    @router.message(ScheduleState.waiting_time_input)
    async def time_input(message: Message, state: FSMContext):
        txt = message.text.strip()
        # basic validation HH:MM
        try:
            parts = txt.split(":")
            h = int(parts[0])
            m = int(parts[1])
            if not (0 <= h < 24 and 0 <= m < 60):
                raise ValueError()
        except Exception:
            await message.answer("Неверный формат времени. Введи HH:MM")
            return
        service.set_edit_time(message.from_user.id, txt)
        s = service.schedule_edits.get(message.from_user.id)
        await message.answer("Время сохранено", reply_markup=schedule_kb(s.get("days"), s.get("time")))
        await state.clear()

    return router
