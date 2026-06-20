#!/usr/bin/env python
import os
import sys
import time
import socket
import subprocess

# Wait for PostgreSQL to be ready before migrations
def wait_for_postgres(host: str, port: int, timeout: int = 30) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except OSError:
            time.sleep(1)
    return False

postgres_host = os.getenv("POSTGRES_SERVER", "db")
if not wait_for_postgres(postgres_host, 5432):
    print(f"❌ Unable to connect to PostgreSQL at {postgres_host}:5432 after waiting, exiting.")
    sys.exit(1)

# Apply database migrations
subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)

# Start FastAPI server
subprocess.run([
    sys.executable,
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
], check=True)
