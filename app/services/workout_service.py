class WorkoutService:
    def __init__(self, repo):
        self.repo = repo
        self.sessions = {}
        self.schedule_edits = {}
        
    def validate_time(self, time_str: str) -> bool:
        from datetime import datetime
        if not isinstance(time_str, str):
            return False
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except Exception:
            return False
    async def ensure_user(self, user_id: int):
        user = await self.repo.get_user(user_id)
        if not user:
            await self.repo.create_user(user_id)
            return False
        return True
    async def start_workout(self, user_id: int):
        workout_id = await self.repo.create_workout(user_id)
        plan = await self.get_plan(user_id)
        print("USER PLAN:", plan)
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

        # populate last weights per exercise
        last_weights = {}
        for ex in exercises:
            try:
                lw = await self.repo.get_last_weight(user_id, ex["id"])
            except Exception:
                lw = None
            last_weights[ex["id"]] = lw or 60.0

        self.sessions[user_id] = {
            "current": 0,
            "exercises": exercises,
            "db_ids": db_ids,
            "last_weights": last_weights,
            "current_weight": last_weights[exercises[0]["id"]] if exercises else 60.0
        }
        return self._current(user_id)
    async def add_set(self, user_id, weight, reps):
        s = self.sessions[user_id]
        idx = s["current"]
        ex = s["exercises"][idx]
        await self.repo.add_set(s["db_ids"][idx], weight, reps)
        ex["done"] += 1
        # persist last weight
        try:
            await self.repo.set_last_weight(user_id, ex["id"], weight)
            s["last_weights"][ex["id"]] = weight
        except Exception:
            pass
        if ex["done"] >= ex["sets"]:
            s["current"] += 1
            if s["current"] >= len(s["exercises"]):
                del self.sessions[user_id]
                return {"status": "finished"}
        # update current_weight for next exercise
        cur = s["current"]
        if cur < len(s["exercises"]):
            next_ex_id = s["exercises"][cur]["id"]
            s["current_weight"] = s["last_weights"].get(next_ex_id, s.get("current_weight", 60.0))
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
    async def set_schedule(self, user_id: int, days: str, notify_time: str):
        await self.repo.set_schedule(user_id, days, notify_time)
    async def get_schedule(self, user_id: int):
        return await self.repo.get_schedule(user_id)
    async def get_plan(self, user_id: int):
        return await self.repo.get_plan(user_id)
    async def get_schedule(self, user_id: int):
        return await self.repo.get_schedule(user_id)

    # schedule edit helpers (ephemeral)
    def start_schedule_edit(self, user_id: int, current=None):
        if current is None:
            current = {"days": ["Mon", "Wed", "Fri"], "time": "17:00"}
        self.schedule_edits[user_id] = {"days": current.get("days", []), "time": current.get("time", "17:00")}
        return self.schedule_edits[user_id]

    def toggle_edit_day(self, user_id: int, day: str):
        s = self.schedule_edits.get(user_id)
        if not s:
            s = self.start_schedule_edit(user_id)
        days = s["days"]
        if day in days:
            days.remove(day)
        else:
            days.append(day)
        s["days"] = days
        return s

    def set_edit_time(self, user_id: int, time_str: str):
        s = self.schedule_edits.get(user_id)
        if not s:
            s = self.start_schedule_edit(user_id)
        s["time"] = time_str
        return s

    async def save_schedule_edit(self, user_id: int):
        s = self.schedule_edits.get(user_id)
        if not s:
            return False
        # validate time format before saving
        if not self.validate_time(s.get("time", "")):
            return False
        days = ",".join(s["days"])
        await self.set_schedule(user_id, days, s["time"])
        del self.schedule_edits[user_id]
        return True

    # history / stats wrappers
    async def get_history(self, user_id: int, limit: int = 10):
        return await self.repo.get_workout_history(user_id, limit)

    async def get_stats(self, user_id: int):
        return await self.repo.get_user_stats(user_id)