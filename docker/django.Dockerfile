# Stage 1: Build dependency wheels
FROM python:3.13-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final runner image
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . .

# Ensure staticfiles and media directories exist for Gunicorn
RUN mkdir -p /app/staticfiles /app/media

# Create non-root user
RUN addgroup --system django && adduser --system --group django
RUN chown -R django:django /app

USER django

EXPOSE 8000
