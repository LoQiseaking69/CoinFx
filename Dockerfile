# ✅ Use a lightweight, optimized Python 3.10 base image
FROM python:3.10-slim

# ✅ Set environment variables
ENV PYTHONUNBUFFERED=1 \
    TZ=UTC \
    DISPLAY=:0 \
    XAUTHORITY=/tmp/.docker.xauth \
    VENV_PATH="/app/venv" \
    PATH="/app/venv/bin:$PATH"

# ✅ Set working directory
WORKDIR /app

# ✅ Install required system dependencies (Minimal GUI & Essentials)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-venv python3-tk libxcb1 tk-dev libxt6 libxrender1 libx11-6 \
    libxss1 libgl1-mesa-glx libglib2.0-0 x11-xserver-utils x11-apps xauth \
    dbus-x11 xdg-utils libxkbcommon-x11-0 \
    git curl unzip libssl-dev libffi-dev libsqlite3-dev util-linux uuid-runtime \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy project files (So we can install dependencies from them)
COPY . .

# ✅ Create & verify venv, then install all dependencies in one layer
RUN python3 -m venv /app/venv \
 && /app/venv/bin/python -m ensurepip --default-pip \
 && /app/venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
 && /app/venv/bin/python -m pip install --no-cache-dir \
    numpy scipy tensorflow-cpu keras pandas \
    scikit-learn websocket-client websockets grpcio protobuf python-dotenv requests \
    ccxt pyjwt cryptography matplotlib ipywidgets flask fastapi uvicorn \
 && /app/venv/bin/python -m pip uninstall -y six \
 && /app/venv/bin/python -m pip install --no-cache-dir six>=1.12.0 \
 && /app/venv/bin/python -m pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git \
 && rm -rf /app/.cache /root/.cache /tmp/pip* /var/lib/apt/lists/*

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Create a non-root user for security & set permissions
RUN useradd -m dockeruser && chown -R dockeruser /app /app/venv

# ✅ Inject X11 GUI setup & authentication into the startup process
RUN echo '#!/bin/bash' > /startup.sh && \
    echo 'echo "🔥 Allowing X11 connections..."' >> /startup.sh && \
    echo 'xhost +local:docker' >> /startup.sh && \
    echo 'echo "🖥️ Setting up X11 authentication..."' >> /startup.sh && \
    echo 'touch /tmp/.docker.xauth' >> /startup.sh && \
    echo 'xauth generate "$DISPLAY" . trusted' >> /startup.sh && \
    echo 'xauth add "$DISPLAY" . $(uuidgen)' >> /startup.sh && \
    echo 'chown dockeruser:dockeruser /tmp/.docker.xauth' >> /startup.sh && \
    echo 'echo "🚀 Launching application..."' >> /startup.sh && \
    echo 'exec /app/venv/bin/python /app/main.py' >> /startup.sh && \
    chmod +x /startup.sh

# ✅ Create `fxcbot` script globally BEFORE switching users
RUN echo '#!/bin/bash' > /usr/local/bin/fxcbot && \
    echo 'xhost +local:docker' | tee -a /etc/bash.bashrc && \
    echo 'docker run --rm -it -e DISPLAY=$DISPLAY -e XAUTHORITY=/tmp/.docker.xauth -v /tmp/.X11-unix:/tmp/.X11-unix -v /tmp/.docker.xauth:/tmp/.docker.xauth --name coinfx-trading-bot coinfx-trading-bot:latest "$@"' >> /usr/local/bin/fxcbot && \
    chmod +x /usr/local/bin/fxcbot

# ✅ Ensure `xhost` commands persist for GUI visibility
RUN echo "xhost +local:docker" >> /etc/bash.bashrc

# ✅ Switch to non-root user for security
USER dockeruser

# ✅ Expose port 5000 for Flask, FastAPI, or WebSocket services
EXPOSE 5000

# ✅ Single command execution for GUI setup & bot launch
ENTRYPOINT ["/bin/bash", "/startup.sh"]