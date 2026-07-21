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
