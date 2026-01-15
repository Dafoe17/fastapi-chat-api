FROM python:3.13-slim

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

COPY README.md ./

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY src ./src
COPY tests ./tests
COPY alembic.ini ./alembic.ini
COPY src/migrations ./src/migrations
COPY .env.example .env

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
