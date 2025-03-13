# ✅ Use a lightweight, optimized Python 3.9 base image
FROM python:3.9-slim

# ✅ Set environment variables
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# ✅ Copy project files into the container
COPY . .

# ✅ Install required system dependencies (including Tkinter, venv, and WebSocket support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-venv python3-tk libxcb1 tk-dev libxt6 libxrender1 libx11-6 \
    libxss1 git curl unzip libssl-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ Ensure venv is created correctly with Python 3
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip

# ✅ Set the virtual environment path
ENV PATH="/app/venv/bin:$PATH"

# ✅ Install all dependencies inside the virtual environment
RUN pip install --no-cache-dir numpy scipy tensorflow keras pandas \
    scikit-learn websocket-client websockets grpcio protobuf python-dotenv requests \
    cbpro ccxt pyjwt cryptography matplotlib ipywidgets flask fastapi uvicorn \
    && pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Expose port 5000 for Flask, FastAPI, or WebSocket services
EXPOSE 5000

# ✅ Define the default command to run the bot inside the virtual environment
CMD ["/app/venv/bin/python", "main.py"]
