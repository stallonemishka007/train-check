FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir aiogram asyncpg alembic
CMD ["sh", "-c", "alembic upgrade head && python -m app.main"]