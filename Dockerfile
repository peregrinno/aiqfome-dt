FROM ghcr.io/astral-sh/uv:0.8.20-python3.11-trixie-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .

RUN uv venv

RUN uv pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "webserver:app", "--host", "0.0.0.0", "--port", "8000"]
