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
    git curl unzip libssl-dev libffi-dev libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# ✅ Create & verify virtual environment with `pip`
RUN python3 -m venv ${VENV_PATH} && \
    ${VENV_PATH}/bin/python -m ensurepip --default-pip && \
    ${VENV_PATH}/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    test -f "${VENV_PATH}/bin/pip" || (${VENV_PATH}/bin/python -m ensurepip && ${VENV_PATH}/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel)

# ✅ Copy project files after setting up venv (Optimizes caching)
COPY . .

# ✅ Install dependencies inside the virtual environment
RUN ${VENV_PATH}/bin/python -m pip install --no-cache-dir \
    numpy scipy tensorflow-cpu keras pandas \
    scikit-learn websocket-client websockets grpcio protobuf python-dotenv requests \
    ccxt pyjwt cryptography matplotlib ipywidgets flask fastapi uvicorn \
    && ${VENV_PATH}/bin/python -m pip uninstall -y six && ${VENV_PATH}/bin/python -m pip install --no-cache-dir six>=1.12.0 \
    && ${VENV_PATH}/bin/python -m pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git \
    && rm -rf ~/.cache/pip  # ✅ Reduce image size by clearing pip cache

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Create a non-root user for security
RUN useradd -m dockeruser && chown -R dockeruser /app

# ✅ Inject X11 GUI setup & authentication into the startup process
RUN echo '#!/bin/bash' > /startup.sh && \
    echo 'echo "🔥 Allowing X11 connections..."' >> /startup.sh && \
    echo 'xhost +local:docker' >> /startup.sh && \
    echo 'echo "🖥️ Setting up X11 authentication..."' >> /startup.sh && \
    echo 'touch /tmp/.docker.xauth' >> /startup.sh && \
    echo 'xauth generate :0 . trusted' >> /startup.sh && \
    echo 'xauth add :0 . $(mcookie)' >> /startup.sh && \
    echo 'chown dockeruser:dockeruser /tmp/.docker.xauth' >> /startup.sh && \
    echo 'exec /app/venv/bin/python /app/main.py' >> /startup.sh && \
    chmod +x /startup.sh

# ✅ Create `fxcbot` script globally BEFORE switching users
RUN echo '#!/bin/bash' > /usr/local/bin/fxcbot && \
    echo 'xhost +local:docker' | tee -a /etc/bash.bashrc && \
    echo 'docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /tmp/.docker.xauth:/tmp/.docker.xauth -e XAUTHORITY=/tmp/.docker.xauth --name coinfx-trading-bot ghcr.io/loqiseaking69/coinfx-trading-bot:latest "$@"' >> /usr/local/bin/fxcbot && \
    chmod +x /usr/local/bin/fxcbot

# ✅ Fix `xhost` issues for GUI applications
RUN echo "xhost +local:docker" >> /etc/bash.bashrc

# ✅ Switch to non-root user for security
USER dockeruser

# ✅ Expose port 5000 for Flask, FastAPI, or WebSocket services
EXPOSE 5000

# ✅ Single command execution for GUI setup & bot launch
ENTRYPOINT ["/bin/bash", "/startup.sh"]