rom aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def today_kb(workout_id):
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(
text=“▶️ Начать тренировку”,
callback_data=f”ws:start:{workout_id}”
)]
])

def exercise_kb(ex_id, workout_id):
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(
text=“✅ Добавить подход”,
callback_data=f”set:add:{ex_id}”
)],
[InlineKeyboardButton(
text=“➡️ Следующее упражнение”,
callback_data=f”we:next:{workout_id}”
)]
])

def finish_kb(workout_id):
return InlineKeyboardMarkup(inline_keyboard=[
[InlineKeyboardButton(
text=“🏁 Завершить тренировку”,
callback_data=f”ws:finish:{workout_id}”
)]
])