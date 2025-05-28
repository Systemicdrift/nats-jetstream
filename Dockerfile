FROM python:3.13-slim

# Install system dependencies and curl
# RUN apt-get update && apt-get install -y \
#     curl \
#     build-essential \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# Install uv via Astral's installer
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy working files
WORKDIR /app
COPY . .

# Install the application dependencies.
RUN uv sync --frozen --no-cache
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

# Run the app
# CMD ["uv", "run", "main.py"]
CMD ["python", "-m", "uvicorn", "app.services:app", "--host", "0.0.0.0", "--port", "8000"]