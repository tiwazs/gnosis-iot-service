FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY migrations ./migrations
COPY app ./app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 3000

CMD ["sh", "-c", "alembic upgrade head && exec uvicorn main:app --app-dir app --host ${SERVER_HOST:-0.0.0.0} --port ${SERVER_PORT:-3000}"]
