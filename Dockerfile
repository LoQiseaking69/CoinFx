# ✅ Use a lightweight, optimized Python 3.10 base image
FROM python:3.10-slim

# ✅ Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TZ=UTC \
    DISPLAY=:0 \
    PATH="/app/venv/bin:$PATH"

# ✅ Set working directory
WORKDIR /app

# ✅ Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-venv python3-tk libxcb1 tk-dev libxt6 libxrender1 libx11-6 \
    libxss1 libgl1-mesa-glx libglib2.0-0 x11-xserver-utils x11-apps xauth \
    git curl unzip libssl-dev libffi-dev libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ Create a virtual environment & upgrade pip
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel

# ✅ Copy project files after setting up venv (Optimizes caching)
COPY . .

# ✅ Install dependencies inside the virtual environment
RUN /app/venv/bin/pip install --no-cache-dir \
    numpy scipy tensorflow-cpu keras pandas \
    scikit-learn websocket-client websockets grpcio protobuf python-dotenv requests \
    ccxt pyjwt cryptography matplotlib ipywidgets flask fastapi uvicorn \
    && /app/venv/bin/pip uninstall -y six && /app/venv/bin/pip install --no-cache-dir six>=1.12.0 \
    && /app/venv/bin/pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git \
    && rm -rf ~/.cache/pip  # ✅ Reduce image size by clearing pip cache

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Create a non-root user for security
RUN useradd -m dockeruser && chown -R dockeruser /app

# ✅ Create `fxcbot` script globally BEFORE switching users
RUN echo '#!/bin/bash' > /usr/local/bin/fxcbot && \
    echo 'docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name coinfx-trading-bot ghcr.io/loqiseaking69/coinfx-trading-bot:latest "$@"' >> /usr/local/bin/fxcbot && \
    chmod +x /usr/local/bin/fxcbot

# ✅ Fix `xhost` issues for GUI applications
RUN echo "xhost +local:docker" >> /etc/bash.bashrc

# ✅ Switch to non-root user for security
USER dockeruser

# ✅ Expose port 5000 for Flask, FastAPI, or WebSocket services
EXPOSE 5000

# ✅ Run inside the virtual environment to ensure dependencies are available
CMD ["/app/venv/bin/python", "main.py"]
