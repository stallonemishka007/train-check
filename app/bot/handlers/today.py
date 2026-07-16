from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.inline import today_kb


def get_router(service):
    router = Router()


        @router.message(Command("today"))
        async def today_cmd(message: Message):
            workout = await service.get_or_create_today()
            await message.answer(
            f"Сегодня\nТренировка {workout['type']}", reply_markup=today_kb(workout["id"])
            )


        @router.callback_query(lambda c: c.data == "today")
        async def today_cb(callback: CallbackQuery):
            workout = await service.get_or_create_today()
            await callback.message.answer(
            f"Сегодня\nТренировка {workout['type']}", reply_markup=today_kb(workout["id"])
            )
            await callback.answer()


return router
