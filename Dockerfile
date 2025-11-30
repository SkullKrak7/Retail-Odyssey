# Multi-arch build for ARM64 (Raspberry Pi 4/5, Apple Silicon)
FROM --platform=$BUILDPLATFORM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run
CMD ["python", "-m", "src.api.main"]
