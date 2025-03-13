# Use a lightweight Python 3.9 image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy all files
COPY . .

# Install required system dependencies (including Tkinter)
RUN apt-get update && apt-get install -y \
    build-essential libopenblas-dev liblapack-dev libx11-6 git \
    python3-tk libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy scipy tensorflow keras pandas scikit-learn websocket-client grpcio protobuf python-dotenv requests && \
    (pip install --no-cache-dir cbpro || pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git)

# Expose port 5000 for Flask or FastAPI apps
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
