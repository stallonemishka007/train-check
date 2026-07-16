class WorkoutRepository:
def init(self, pool):
self.pool = pool

# --- получить тренировку на сегодня ---
async def get_today(self, today):
    async with self.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM workouts WHERE workout_date = $1",
            today
        )
        return dict(row) if row else None
# --- последняя тренировка ---
async def get_last_workout(self):
    async with self.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT * FROM workouts
            ORDER BY workout_date DESC, id DESC
            LIMIT 1
            """
        )
        return dict(row) if row else None
# --- создать тренировку ---
async def create_workout(self, workout_date, workout_type):
    async with self.pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO workouts (workout_date, type, status)
            VALUES ($1, $2, 'planned')
            RETURNING *
            """,
            workout_date,
            workout_type
        )
        return dict(row)
# --- получить templates ---
async def get_templates(self, workout_type):
    async with self.pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM exercise_templates
            WHERE workout_type = $1
            ORDER BY order_index
            """,
            workout_type
        )
        return [dict(r) for r in rows]
# --- создать упражнения в тренировке ---
async def create_workout_exercises(self, workout_id, templates):
    async with self.pool.acquire() as conn:
        for t in templates:
            await conn.execute(
                """
                INSERT INTO workout_exercises (
                    workout_id,
                    template_id,
                    name,
                    order_index,
                    planned_sets,
                    reps_min,
                    reps_max,
                    planned_weight
                )
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
                """,
                workout_id,
                t["id"],
                t["name"],
                t["order_index"],
                t["sets"],
                t["reps_min"],
                t["reps_max"],
                t["weight"]
            )
# --- получить упражнения тренировки ---
async def get_workout_exercises(self, workout_id):
    async with self.pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM workout_exercises
            WHERE workout_id = $1
            ORDER BY order_index
            """,
            workout_id
        )
        return [dict(r) for r in rows]
# --- получить одно упражнение ---
async def get_exercise(self, exercise_id):
    async with self.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM workout_exercises WHERE id = $1",
            exercise_id
        )
        return dict(row)
# --- добавить подход ---
async def add_set(self, exercise_id, reps, weight):
    async with self.pool.acquire() as conn:
        count = await conn.fetchval(
            "SELECT COUNT(*) FROM exercise_sets WHERE workout_exercise_id = $1",
            exercise_id
        )
        await conn.execute(
            """
            INSERT INTO exercise_sets (workout_exercise_id, set_number, reps, weight)
            VALUES ($1,$2,$3,$4)
            """,
            exercise_id,
            count + 1,
            reps,
            weight
        )
# --- посчитать подходы ---
async def count_sets(self, exercise_id):
    async with self.pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT COUNT(*) FROM exercise_sets WHERE workout_exercise_id = $1",
            exercise_id
        )
# --- старт тренировки ---
async def start_workout(self, workout_id):
    async with self.pool.acquire() as conn:
        await conn.execute(
            "UPDATE workouts SET status='in_progress', started_at=NOW() WHERE id=$1",
            workout_id
        )
# --- завершить тренировку ---
async def finish_workout(self, workout_id):
    async with self.pool.acquire() as conn:
        await conn.execute(
            "UPDATE workouts SET status='done', completed_at=NOW() WHERE id=$1",
            workout_id
        )