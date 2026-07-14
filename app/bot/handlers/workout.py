from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
def get_router(workout_service):
    router = Router()
    # --- /start ---
    @router.message(Command("start"))
    async def start(message: Message):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📅 Сегодня", callback_data="today")]
        ])
        await message.answer("Главное меню", reply_markup=kb)
    # --- today ---
    @router.callback_query(F.data == "today")
    async def today(callback: CallbackQuery):
        workout = await workout_service.get_today_workout()
        if not workout:
            await callback.message.answer("Сегодня нет тренировки")
            await callback.answer()
            return
        text = f"Тренировка {workout['type']}\nСтатус: {workout['status']}"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="▶️ Начать",
                callback_data=f"ws:start:{workout['id']}"
            )]
        ])
        await callback.message.answer(text, reply_markup=kb)
        await callback.answer()
    # --- start workout ---
    @router.callback_query(F.data.startswith("ws:start:"))
    async def start_workout(callback: CallbackQuery):
        _, _, workout_id = callback.data.split(":")
        workout_id = int(workout_id)
        ex = await workout_service.start_workout(workout_id)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Добавить подход",
                callback_data=f"set:add:{ex['id']}"
            )],
            [InlineKeyboardButton(
                text="➡️ Следующее",
                callback_data=f"we:next:{workout_id}"
            )]
        ])
        await callback.message.answer(
            f"{ex['name']}\n{ex['done']}/{ex['sets']} подходов",
            reply_markup=kb
        )
        await callback.answer()
    # --- open exercise ---
    @router.callback_query(F.data.startswith("we:open:"))
    async def open_exercise(callback: CallbackQuery):
        _, _, ex_id = callback.data.split(":")
        ex_id = int(ex_id)
        ex = await workout_service.get_exercise(ex_id)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Добавить подход",
                callback_data=f"set:add:{ex_id}"
            )]
        ])
        await callback.message.answer(
            f"{ex['name']}\n{ex['done']}/{ex['sets']} подходов",
            reply_markup=kb
        )
        await callback.answer()
    # --- add set ---
    @router.callback_query(F.data.startswith("set:add:"))
    async def add_set(callback: CallbackQuery):
        _, _, ex_id = callback.data.split(":")
        ex_id = int(ex_id)
        result = await workout_service.add_set(ex_id)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Ещё подход",
                callback_data=f"set:add:{ex_id}"
            )],
            [InlineKeyboardButton(
                text="➡️ Далее",
                callback_data=f"we:next:{result['workout_id']}"
            )]
        ])
        await callback.message.answer(
            f"Подход добавлен ✅\n{result['done']}/{result['total']}",
            reply_markup=kb
        )
        await callback.answer()
    # --- next exercise ---
    @router.callback_query(F.data.startswith("we:next:"))
    async def next_exercise(callback: CallbackQuery):
        _, _, workout_id = callback.data.split(":")
        workout_id = int(workout_id)
        ex = await workout_service.next_exercise(workout_id)
        if not ex:
            await callback.message.answer("Все упражнения выполнены ✅")
            await callback.answer()
            return
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Добавить подход",
                callback_data=f"set:add:{ex['id']}"
            )]
        ])
        await callback.message.answer(
            f"{ex['name']}\n{ex['done']}/{ex['sets']}",
            reply_markup=kb
        )
        await callback.answer()
    # --- finish workout ---
    @router.callback_query(F.data.startswith("ws:finish:"))
    async def finish_workout(callback: CallbackQuery):
        _, _, workout_id = callback.data.split(":")
        workout_id = int(workout_id)
        await workout_service.finish_workout(workout_id)
        await callback.message.answer("Тренировка завершена ✅")
        await callback.answer()
    return router
@router.message(Command("today"))
async def today_cmd(message: Message):
    workout = await workout_service.get_or_create_today()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▶️ Начать тренировку",
            callback_data=f"ws:start:{workout['id']}"
        )]
    ])
    await message.answer(
        f"Сегодня\nТренировка {workout['type']}\nСтатус: {workout['status']}",
        reply_markup=kb
    )
@router.callback_query(F.data == "today")
async def today_cb(callback: CallbackQuery):
    workout = await workout_service.get_or_create_today()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▶️ Начать тренировку",
            callback_data=f"ws:start:{workout['id']}"
        )]
    ])
    await callback.message.answer(
        f"Сегодня\nТренировка {workout['type']}\nСтатус: {workout['status']}",
        reply_markup=kb
    )
    await callback.answer()
