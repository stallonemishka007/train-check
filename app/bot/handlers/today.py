from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.keyboards.inline import today_kb
def get_router(service):
    router = Router()
    @router.message(Command("today"))
    async def today_cmd(message: Message):
        workout = await service.get_today_workout(message.from_user.id)
        await message.answer(
            f"Сегодня\n{workout['name']}",
            reply_markup=today_kb(workout["id"])
        )
    return router