class WorkoutService:
    def __init__(self, repo):
        self.repo = repo
        self.sessions = {}
    async def start_workout(self, user_id: int):
        workout_id = await self.repo.create_workout(user_id)
        exercises = [
            {"id": 1, "name": "Жим лёжа", "sets": 4, "done": 0},
            {"id": 2, "name": "Присед", "sets": 3, "done": 0}
        ]
        db_ids = []
        for i, ex in enumerate(exercises):
            db_id = await self.repo.add_exercise(workout_id, ex["id"], i)
            db_ids.append(db_id)
        self.sessions[user_id] = {
            "workout_id": workout_id,
            "current": 0,
            "exercises": exercises,
            "db_ids": db_ids
        }
        return self._current(user_id)
    async def add_set(self, user_id: int, weight: float, reps: int):
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
    def _current(self, user_id: int):
        s = self.sessions[user_id]
        ex = s["exercises"][s["current"]]
        return {
            "id": ex["id"],
            "name": ex["name"],
            "done": ex["done"],
            "sets": ex["sets"],
            "index": s["current"] + 1,
            "total": len(s["exercises"])
        }