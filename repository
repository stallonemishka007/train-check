class WorkoutRepository:
    def __init__(self, pool):
        self.pool = pool
    async def get_workout(self, workout_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM workouts WHERE id=$1",
                workout_id
            )
    async def insert_set(self, workout_id, name, reps, weight):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO sets (workout_id, exercise_name, reps, weight)
                VALUES ($1, $2, $3, $4)
                """,
                workout_id, name, reps, weight
            )
    async def count_sets(self, workout_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT COUNT(*) FROM sets WHERE workout_id=$1",
                workout_id
            )