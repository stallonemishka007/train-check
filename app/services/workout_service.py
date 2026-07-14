from app.domain.workout_logic import calculate_status
from app.domain.progression import get_next_set
WORKOUTS = {
    "A": [
        {"name": "Жим", "sets": 3, "reps": "8-10", "weight": 10}
    ]
}
class WorkoutService
    def __init__(self, repo)
        self.repo = repo
    async def add_set(self, workout_id, ex_index)
        workout = await self.repo.get_workout(workout_id)
        ex = WORKOUTS[workout[type]][ex_index]
        reps, weight = get_next_set(None, ex)
        await self.repo.insert_set(workout_id, ex[name], reps, weight)
        done = await self.repo.count_sets(workout_id)
        total = ex[sets]
        status = calculate_status(done, total)
        return status