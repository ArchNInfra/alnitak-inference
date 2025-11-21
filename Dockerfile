FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system deps (optional, minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose API port
EXPOSE 8000

# Startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
