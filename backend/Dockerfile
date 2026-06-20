# syntax=docker/dockerfile:1

# -------- Backend Build Stage --------
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for caching
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Run Alembic migrations (will also be executed at runtime)
# In production we will run migrations on container startup via entrypoint script.

# -------- Backend Runtime Stage --------
FROM python:3.12-slim AS runtime
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

# Entrypoint script to run migrations then start the server
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Add a non‑root user for security
RUN adduser --uid 1001 --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

# Environment variables (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
