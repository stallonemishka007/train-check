from datetime import date
class WorkoutService:
    def __init__(self, repo):
        self.repo = repo
    # --- создать тренировку из шаблона ---
    async def create_today_workout(self, workout_type):
        workout = await self.repo.create_workout(date.today(), workout_type)
        templates = await self.repo.get_templates(workout_type)
        await self.repo.create_workout_exercises(
            workout["id"],
            templates
        )
        return workout
    # --- старт ---
    async def start_workout(self, workout_id):
        await self.repo.start_workout(workout_id)
        exercises = await self.repo.get_workout_exercises(workout_id)
        first = exercises[0]
        done = await self.repo.count_sets(first["id"])
        return {
            "id": first["id"],
            "name": first["name"],
            "sets": first["planned_sets"],
            "done": done
        }
    # --- открыть упражнение ---
    async def get_exercise(self, ex_id):
        ex = await self.repo.get_exercise(ex_id)
        done = await self.repo.count_sets(ex_id)
        return {
            "id": ex_id,
            "name": ex["name"],
            "sets": ex["planned_sets"],
            "done": done
        }
    # --- добавить подход ---
    async def add_set(self, ex_id):
        ex = await self.repo.get_exercise(ex_id)
        reps = ex["reps_min"] or 10
        weight = ex["planned_weight"] or 10
        await self.repo.add_set(ex_id, reps, weight)
        done = await self.repo.count_sets(ex_id)
        return {
            "done": done,
            "total": ex["planned_sets"]
        }
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
                    "done": done
                }
        return None
    async def finish_workout(self, workout_id):
        await self.repo.finish_workout(workout_id)