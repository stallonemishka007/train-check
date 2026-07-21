class WorkoutService:
    def __init__(self, repo):
        self.repo = repo
        self.sessions = {}
    async def ensure_user(self, user_id: int):
        user = await self.repo.get_user(user_id)
        if not user:
            await self.repo.create_user(user_id)
            return False
        return True
    async def start_workout(self, user_id: int):
        workout_id = await self.repo.create_workout(user_id)
        plan = await self.get_plan(user_id)
        if plan == "full":
            exercises = [
                {"id": 1, "name": "Жим лёжа", "sets": 4, "done": 0},
                {"id": 2, "name": "Присед", "sets": 3, "done": 0}
            ]
        elif plan == "split":
            exercises = [
                {"id": 1, "name": "Жим лёжа", "sets": 4, "done": 0}
            ]
        else:
            # fallback
            exercises = [
                {"id": 1, "name": "Жим лёжа", "sets": 4, "done": 0}
            ]
        db_ids = []
        for i, ex in enumerate(exercises):
            db_id = await self.repo.add_exercise(workout_id, ex["id"], i)
            db_ids.append(db_id)
        self.sessions[user_id] = {
            "current": 0,
            "exercises": exercises,
            "db_ids": db_ids
        }
        return self._current(user_id)
    async def add_set(self, user_id, weight, reps):
        s = self.sessions[user_id]
        idx = s["current"]
        ex = s["exercises"][idx]
        await self.repo.add_set(s["db_ids"][idx], weight, reps)
        ex["done"] += 1
        if ex["done"] >= ex["sets"]:
            s["current"] += 1
            if s["current"] >= len(s["exercises"]):
                del self.sessions[user_id]
                return {"status": "finished"}
        return self._current(user_id)
    def _current(self, user_id):
        s = self.sessions[user_id]
        ex = s["exercises"][s["current"]]
        return {
            "id": ex["id"],
            "name": ex["name"],
            "done": ex["done"],
            "sets": ex["sets"]
        }
    async def set_plan(self, user_id: int, plan: str):
        await self.repo.set_plan(user_id, plan)
    async def get_plan(self, user_id: int):
        return await self.repo.get_plan(user_id)