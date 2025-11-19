# ---------------------------
# 1. Base Image
# ---------------------------
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ---------------------------
# 2. Working Directory
# ---------------------------
WORKDIR /app

# ---------------------------
# 3. Copy requirements first (better caching)
# ---------------------------
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------------------------
# 4. Copy the application code
# ---------------------------
COPY src ./src
COPY run.sh .
COPY README.md .
COPY LICENSE .

# Make run script executable (optional)
RUN chmod +x run.sh

# ---------------------------
# 5. Create non-root user (security)
# ---------------------------
RUN useradd -m appuser
USER appuser

# ---------------------------
# 6. Expose Port
# ---------------------------
EXPOSE 8000

# ---------------------------
# 7. Command to start server
# ---------------------------
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
