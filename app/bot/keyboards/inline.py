from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def today_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🏋️ Начать тренировку",
                callback_data="start"
            )]
        ]
    )
def exercise_kb(exercise_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Подход",
                callback_data=f"set:{exercise_id}"
            )]
        ]
    )