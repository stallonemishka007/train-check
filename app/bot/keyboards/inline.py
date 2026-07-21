from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️ Начать тренировку", callback_data="start")]
    ])
def plan_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💪 Фулбоди", callback_data="plan:full")],
        [InlineKeyboardButton(text="🏋️ Верх/Низ", callback_data="plan:split")]
    ])
def exercise_kb(ex_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подход", callback_data=f"set:{ex_id}")]
    ])