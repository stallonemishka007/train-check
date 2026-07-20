from aiogram.fsm.state import StatesGroup, State
class WorkoutState(StatesGroup):
    waiting_input = State()