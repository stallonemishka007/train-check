from datetime import date

class WorkoutService:
    def __init__(self, repo):
        self.repo = repo
        self.sessions = {}  # {user_id: session}
    async def get_today_workout(self, user_id: int):
        return {
            "id": 1,
            "name": "Тренировка дня"
        }
    async def start_workout(self, user_id: int, workout_id: int):
        session = {
            "workout_id": workout_id,
            "current_exercise": 0,
            "exercises": [
                {"id": 1, "name": "Жим лёжа", "sets": 4, "done": 0},
                {"id": 2, "name": "Присед", "sets": 3, "done": 0}
            ]
        }
        self.sessions[user_id] = session
        return self._current_exercise(user_id)
    async def add_set(self, user_id: int, exercise_id: int):
        session = self.sessions.get(user_id)
        if not session:
            return {"error": "no active workout"}
        idx = session["current_exercise"]
        ex = session["exercises"][idx]
        # защита: проверяем что жмут на текущее упражнение
        if ex["id"] != exercise_id:
            return self._current_exercise(user_id)
        ex["done"] += 1
        # если ещё не закончили подходы
        if ex["done"] < ex["sets"]:
            return self._format_ex(ex)
        # если закончили упражнение → следующее
        session["current_exercise"] += 1
        # если тренировка закончена
        if session["current_exercise"] >= len(session["exercises"]):
            del self.sessions[user_id]
            return {"status": "finished"}
        return self._current_exercise(user_id)
    def _current_exercise(self, user_id: int):
        session = self.sessions[user_id]
        idx = session["current_exercise"]
        ex = session["exercises"][idx]
        return self._format_ex(ex)
    def _format_ex(self, ex):
        return {
            "id": ex["id"],
            "name": ex["name"],
            "done": ex["done"],
            "total": ex["sets"]
        }