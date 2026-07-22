class WorkoutRepo:
    def __init__(self, pool):
        self.pool = pool
    async def create_user(self, user_id: int):
        query = """
        INSERT INTO users (id) VALUES ($1)
        ON CONFLICT DO NOTHING
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id)
    async def get_user(self, user_id: int):
        query = "SELECT id FROM users WHERE id=$1"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, user_id)
    async def create_workout(self, user_id: int):
        query = """
        INSERT INTO workouts (user_id, started_at)
        VALUES ($1, NOW()) RETURNING id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            return row["id"]
    async def add_exercise(self, workout_id, exercise_id, order_index):
        query = """
        INSERT INTO workout_exercises (workout_id, exercise_id, order_index)
        VALUES ($1, $2, $3) RETURNING id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, workout_id, exercise_id, order_index)
            return row["id"]
    async def add_set(self, we_id, weight, reps):
        query = """
        INSERT INTO sets (workout_exercise_id, weight, reps)
        VALUES ($1, $2, $3)
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, we_id, weight, reps)
    async def set_plan(self, user_id: int, plan: str):
        query = """
        UPDATE users SET plan=$1 WHERE id=$2
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, plan, user_id)
    async def get_plan(self, user_id: int):
        query = "SELECT plan FROM users WHERE id=$1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            return row["plan"] if row else None

    async def set_schedule(self, user_id: int, days: str, notify_time: str):
        query = """
        UPDATE users SET schedule_days=$1, notify_time=$2 WHERE id=$3
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, days, notify_time, user_id)

    async def get_scheduled_users(self):
        query = "SELECT id, schedule_days, notify_time FROM users WHERE schedule_days IS NOT NULL"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
            return [dict(r) for r in rows]

    async def get_schedule(self, user_id: int):
        query = "SELECT schedule_days, notify_time FROM users WHERE id=$1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            if not row:
                return None
            return {"days": row["schedule_days"], "time": row["notify_time"]}

    async def set_last_weight(self, user_id: int, exercise_id: int, weight: float):
        query = """
        INSERT INTO user_exercise_meta (user_id, exercise_id, last_weight)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id, exercise_id) DO UPDATE SET last_weight = EXCLUDED.last_weight
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, exercise_id, weight)

    async def get_last_weight(self, user_id: int, exercise_id: int):
        query = "SELECT last_weight FROM user_exercise_meta WHERE user_id=$1 AND exercise_id=$2"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id, exercise_id)
            return row["last_weight"] if row else None

    async def get_workout_history(self, user_id: int, limit: int = 10):
        query = """
        SELECT w.id as workout_id, w.started_at, we.id as we_id, e.name, s.weight, s.reps
        FROM workouts w
        LEFT JOIN workout_exercises we ON we.workout_id = w.id
        LEFT JOIN exercises e ON e.id = we.exercise_id
        LEFT JOIN sets s ON s.workout_exercise_id = we.id
        WHERE w.user_id = $1
        ORDER BY w.started_at DESC
        LIMIT $2
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, user_id, limit)
            return [dict(r) for r in rows]

    async def get_user_stats(self, user_id: int):
        query = """
        SELECT
            COUNT(DISTINCT w.id) as workouts_count,
            COUNT(s.id) as sets_count,
            AVG(s.weight) as avg_weight
        FROM workouts w
        LEFT JOIN workout_exercises we ON we.workout_id = w.id
        LEFT JOIN sets s ON s.workout_exercise_id = we.id
        WHERE w.user_id = $1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            return dict(row) if row else {"workouts_count": 0, "sets_count": 0, "avg_weight": None}
