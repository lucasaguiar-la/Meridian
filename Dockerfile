FROM python:3.12-slim

WORKDIR /app

# Install curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command: start the API
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
