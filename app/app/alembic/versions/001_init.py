from alembic import op
import sqlalchemy as sa
revision = '001'
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    op.create_table(
        'workouts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.BigInteger),
        sa.Column('started_at', sa.DateTime)
    )
    op.create_table(
        'exercises',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text)
    )
    op.create_table(
        'workout_exercises',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workout_id', sa.Integer),
        sa.Column('exercise_id', sa.Integer),
        sa.Column('order_index', sa.Integer)
    )
    op.create_table(
        'sets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('workout_exercise_id', sa.Integer),
        sa.Column('weight', sa.Float),
        sa.Column('reps', sa.Integer)
    )
def downgrade():
    op.drop_table('sets')
    op.drop_table('workout_exercises')
    op.drop_table('exercises')
    op.drop_table('workouts')