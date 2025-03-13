# ✅ Use a lightweight, optimized Python 3.10 base image (more stable & efficient)
FROM python:3.10-slim

# ✅ Set environment variables for non-buffered output & correct timezone
ENV PYTHONUNBUFFERED=1 TZ=UTC

# ✅ Set working directory
WORKDIR /app

# ✅ Copy project files into the container
COPY . .

# ✅ Install required system dependencies (Tkinter, SSL, WebSockets, Git, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-venv python3-tk libxcb1 tk-dev libxt6 libxrender1 libx11-6 \
    libxss1 git curl unzip libssl-dev libffi-dev libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ Ensure venv is correctly created & upgraded
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel

# ✅ Set the virtual environment path
ENV PATH="/app/venv/bin:$PATH"

# ✅ Install dependencies with optimized conflict resolution
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver \
    numpy scipy tensorflow keras pandas \
    scikit-learn websocket-client websockets grpcio protobuf python-dotenv requests \
    ccxt pyjwt cryptography matplotlib ipywidgets flask fastapi uvicorn \
    && pip uninstall -y six && pip install six>=1.12.0 \
    && pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git \
    && rm -rf ~/.cache/pip  # ✅ Reduce image size by clearing pip cache

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Expose port 5000 for Flask, FastAPI, or WebSocket services
EXPOSE 5000

# ✅ Define the default command to run the bot inside the virtual environment
CMD ["python", "main.py"]