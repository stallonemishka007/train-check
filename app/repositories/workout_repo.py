class WorkoutRepo:
    def __init__(self, pool):
        self.pool = pool
    async def create_workout(self, user_id: int):
        query = """
        INSERT INTO workouts (user_id, started_at)
        VALUES ($1, NOW()) RETURNING id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            return row["id"]
    async def add_exercise(self, workout_id: int, exercise_id: int, order_index: int):
        query = """
        INSERT INTO workout_exercises (workout_id, exercise_id, order_index)
        VALUES ($1, $2, $3) RETURNING id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, workout_id, exercise_id, order_index)
            return row["id"]
    async def add_set(self, workout_exercise_id: int, weight: float, reps: int):
        query = """
        INSERT INTO sets (workout_exercise_id, weight, reps)
        VALUES ($1, $2, $3)
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, workout_exercise_id, weight, reps)
    async def get_history(self, user_id: int):
        query = """
        SELECT w.id, w.started_at, e.name, s.weight, s.reps
        FROM workouts w
        JOIN workout_exercises we ON we.workout_id = w.id
        JOIN exercises e ON e.id = we.exercise_id
        JOIN sets s ON s.workout_exercise_id = we.id
        WHERE w.user_id = $1
        ORDER BY w.id DESC
        """
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, user_id)