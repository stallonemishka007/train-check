from aiogram.fsm.state import StatesGroup, State
class WorkoutState(StatesGroup):
    waiting_input = State()
    waiting_custom_weight = State()
    waiting_custom_reps = State()


class ScheduleState(StatesGroup):
    waiting_time_input = State()