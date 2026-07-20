from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️ Начать", callback_data="start")]
    ])