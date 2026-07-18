from datetime import date

class WorkoutService:
    def __init__(self, repo):
        self.repo = repo

    async def get_today_workout(self, user_id: int):
        return {"id": 1, "name": "test"}
    async def start_workout(self, workout_id: int):
        return {"status": "started", "workout_id": workout_id}
    async def start_workout(self, workout_id: int):
        return {
            "id":1,
            "name": "Жим лёжа",
            "done": 0,
            "sets": 4
        }
    async def add_set(self, exercise_id: int):
        return {
            "id": exercise_id,
            "name": "Жим лёжа",
            "done": 1,
            "sets": 4
        }

# --- чередование A/B ---
def get_next_type(self, last_type):
    return "B" if last_type == "A" else "A"


# --- получить или создать тренировку ---
    async def get_or_create_today(self):
        today = date.today()
        workout = await self.repo.get_today(today)
        if workout:
            return workout
        last = await self.repo.get_last_workout()
        if last:
            wtype = self.get_next_type(last["type"])
        else:
            wtype = "A"
        workout = await self.repo.create_workout(today, wtype)
        templates = await self.repo.get_templates(wtype)
        await self.repo.create_workout_exercises(workout["id"], templates)
        return workout


# --- старт тренировки ---
    async def start_workout(self, workout_id):
        await self.repo.start_workout(workout_id)
        exercises = await self.repo.get_workout_exercises(workout_id)
        first = exercises[0]
        done = await self.repo.count_sets(first["id"])
        return {
            "id": first["id"],
            "name": first["name"],
            "sets": first["planned_sets"],
            "done": done,
        }


# --- добавить подход ---
    async def add_set(self, ex_id):
        ex = await self.repo.get_exercise(ex_id)
        reps = ex["reps_min"] or 10
        weight = ex["planned_weight"] or 10
        await self.repo.add_set(ex_id, reps, weight)
        done = await self.repo.count_sets(ex_id)
        return {"done": done, "total": ex["planned_sets"]}


# --- следующее упражнение ---
    async def next_exercise(self, workout_id):
        exercises = await self.repo.get_workout_exercises(workout_id)
        for ex in exercises:
            done = await self.repo.count_sets(ex["id"])
            if done < ex["planned_sets"]:
                return {
                    "id": ex["id"],
                    "name": ex["name"],
                    "sets": ex["planned_sets"],
                    "done": done,
               }
        return None


# --- завершение ---
    async def finish_workout(self, workout_id):
        await self.repo.finish_workout(workout_id)
