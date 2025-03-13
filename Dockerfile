# ✅ Use a lightweight, optimized Python 3.9 base image
FROM python:3.9-slim

# ✅ Set environment variables
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# ✅ Copy all project files into the container
COPY . .

# ✅ Install required system dependencies (including Tkinter for GUI compatibility)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libopenblas-dev liblapack-dev libx11-6 git \
    python3-tk libxcb1 tk-dev libxt6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# ✅ Upgrade pip and install dependencies efficiently
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy scipy tensorflow keras pandas \
    scikit-learn websocket-client grpcio protobuf python-dotenv requests && \
    pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Expose port 5000 for Flask, FastAPI, or WebSocket services
EXPOSE 5000

# ✅ Define the default command to run the bot
CMD ["python", "main.py"]
