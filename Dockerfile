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
COPY . /app/
WORKDIR /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the app
CMD ["uv", "run", "main.py"]