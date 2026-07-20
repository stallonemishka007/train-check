from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def today_kb(workout_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Начать тренировку",
            callback_data=f"start:{workout_id}"
        )]
    ])
def exercise_kb(exercise_id: int, workout_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="✅ Подход",
            callback_data=f"set:{exercise_id}"
        )]
    ])


