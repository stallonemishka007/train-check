from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.bot.keyboards.inline import start_kb
def get_router(service):
    router = Router()
    @router.message(Command("start"))
    async def start(message: Message):
        await message.answer("Готов к тренировке?", reply_markup=start_kb())
    return router