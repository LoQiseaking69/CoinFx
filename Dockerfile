# Use an official Python image with system dependencies
FROM python:3.9-slim

# Set environment variables to prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Ensure correct NumPy and SciPy versions
RUN pip install --no-cache-dir "numpy<1.25.0" "scipy"

# Expose the necessary ports (if needed for API/WebSocket access)
EXPOSE 5000

# Run the trading bot
CMD ["python", "main.py"]