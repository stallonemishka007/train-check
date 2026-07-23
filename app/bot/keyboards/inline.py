from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏋️ Начать тренировку", callback_data="start")],
        [InlineKeyboardButton(text="⚙️ Настроить расписание", callback_data="schedule")]
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


def session_kb(current_weight: float):
    # weight adjust and reps selection
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="-5", callback_data="weight:-5"),
            InlineKeyboardButton(text="-1", callback_data="weight:-1"),
            InlineKeyboardButton(text=f"Вес: {current_weight}kg", callback_data="weight:0"),
            InlineKeyboardButton(text="+1", callback_data="weight:+1"),
            InlineKeyboardButton(text="+5", callback_data="weight:+5"),
        ],
        [
            InlineKeyboardButton(text="6 reps", callback_data="reps:6"),
            InlineKeyboardButton(text="8 reps", callback_data="reps:8"),
            InlineKeyboardButton(text="10 reps", callback_data="reps:10"),
            InlineKeyboardButton(text="12 reps", callback_data="reps:12"),
            InlineKeyboardButton(text="Custom", callback_data="reps:custom"),
        ],
        [InlineKeyboardButton(text="Пропустить упражнение", callback_data="skip")],
        [InlineKeyboardButton(text="Custom вес", callback_data="weight:custom")]
    ])


def schedule_kb(selected_days: list = None, current_time: str = "17:00"):
    if selected_days is None:
        selected_days = ["Mon", "Wed", "Fri"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rows = []
    # create day toggle buttons (one row)
    day_buttons = [InlineKeyboardButton(text=("✅" if d in selected_days else "") + d, callback_data=f"sched:toggle:{d}") for d in days]
    # split into rows of 4
    for i in range(0, len(day_buttons), 4):
        rows.append(day_buttons[i:i+4])
    rows.append([InlineKeyboardButton(text=f"Время: {current_time}", callback_data="sched:time")])
    rows.append([InlineKeyboardButton(text="Сохранить", callback_data="sched:save")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Старт", callback_data="start")],
        [InlineKeyboardButton(text="📋 История", callback_data="history_btn")],
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats_btn")],
        [InlineKeyboardButton(text="⚙️ Расписание", callback_data="schedule")],
        [InlineKeyboardButton(text="💪 Мои упражнения", callback_data="manage_exercises")]
    ])


def manage_exercises_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить упражнение", callback_data="add_exercise")],
        [InlineKeyboardButton(text="📝 Мои упражнения", callback_data="list_exercises")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")]
    ])