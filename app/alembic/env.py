from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import create_engine
from alembic import context
import os
config = context.config
fileConfig(config.config_file_name)
target_metadata = None
def run_migrations_offline():
    context.configure(url=os.getenv("DATABASE_URL"), literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
def run_migrations_online():
    connectable = create_engine(os.getenv("DATABASE_URL"))
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()