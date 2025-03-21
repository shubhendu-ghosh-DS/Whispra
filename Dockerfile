# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for best practices
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory inside the container
WORKDIR /app

# Install system dependencies (optional but useful for certain packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port your app runs on
EXPOSE 7860

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

