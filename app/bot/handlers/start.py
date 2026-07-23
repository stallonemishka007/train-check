from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.bot.keyboards.inline import main_menu_kb
def get_router(service):
    router = Router()
    @router.message(Command("start"))
    async def start(message: Message):
        await service.ensure_user(message.from_user.id)
        await message.answer("👋 Добро пожаловать! Нажмите /start для начала тренировки\n\nГлавное меню", reply_markup=main_menu_kb())
    return router