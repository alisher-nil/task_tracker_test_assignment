FROM python:3.13-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Copy project dependency files
COPY pyproject.toml .
# Install dependencies
RUN pip install --no-cache-dir .

FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install production system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r django && useradd -r -g django django
WORKDIR /app

# Copy installed Python packages
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY . .

# Change ownership to non-root user
RUN chown -R django:django /app

# Switch to non-root user
USER django

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_tracker.wsgi", "--pythonpath", "app"]