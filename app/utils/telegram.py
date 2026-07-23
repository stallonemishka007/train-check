from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest


async def safe_edit_text(callback: CallbackQuery, text: str, reply_markup=None):
    """Safely edit message text, catching 'message is not modified' errors"""
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            # Message hasn't changed, just answer callback
            pass
        else:
            raise
