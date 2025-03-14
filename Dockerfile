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
    libxss1 libgl1-mesa-glx libglib2.0-0 x11-xserver-utils xauth dbus-x11 xdg-utils \
    git curl unzip libssl-dev libffi-dev libsqlite3-dev util-linux uuid-runtime xvfb && \
    rm -rf /var/lib/apt/lists/*

# ✅ Create /tmp/.X11-unix directory with proper permissions (for Xvfb)
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# ✅ Copy project files
COPY . .

# ✅ Create & verify venv, install dependencies in one layer
RUN python3 -m venv /app/venv && \
    /app/venv/bin/python -m ensurepip --default-pip && \
    /app/venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    /app/venv/bin/python -m pip install --no-cache-dir \
       numpy scipy tensorflow-cpu keras pandas scikit-learn websocket-client websockets grpcio protobuf python-dotenv requests \
       ccxt pyjwt cryptography matplotlib ipywidgets flask fastapi uvicorn oandapyV20 && \
    /app/venv/bin/python -m pip uninstall -y six && \
    /app/venv/bin/python -m pip install --no-cache-dir "six>=1.12.0" && \
    /app/venv/bin/python -m pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git && \
    rm -rf /app/.cache /root/.cache /tmp/pip* /var/lib/apt/lists/*

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Create a non-root user for security & set permissions
RUN useradd -m dockeruser && chown -R dockeruser /app /app/venv

# ✅ Consolidate startup scripts into one RUN statement for efficiency
RUN echo '#!/bin/bash' > /startup.sh && \
    echo 'echo "🔥 Allowing X11 connections..."' >> /startup.sh && \
    echo 'xhost +local:docker' >> /startup.sh && \
    echo 'echo "🖥️ Setting up X11 authentication..."' >> /startup.sh && \
    echo 'touch /tmp/.docker.xauth' >> /startup.sh && \
    echo 'xauth generate "$DISPLAY" . trusted' >> /startup.sh && \
    echo 'xauth add "$DISPLAY" . $(xauth list | tail -1 | awk "{print \$3}")' >> /startup.sh && \
    echo 'chown dockeruser:dockeruser /tmp/.docker.xauth' >> /startup.sh && \
    echo 'echo "🚀 Launching application..."' >> /startup.sh && \
    echo 'exec /app/venv/bin/python /app/main.py' >> /startup.sh && \
    chmod +x /startup.sh

# ✅ Create global fxcbot script BEFORE switching users
RUN echo '#!/bin/bash' > /usr/local/bin/fxcbot && \
    echo 'xhost +local:docker' | tee -a /etc/bash.bashrc && \
    echo 'docker run --rm -it -e DISPLAY=$DISPLAY -e XAUTHORITY=/tmp/.docker.xauth -v /tmp/.X11-unix:/tmp/.X11-unix -v /tmp/.docker.xauth:/tmp/.docker.xauth --name coinfx-trading-bot ghcr.io/loqiseaking69/coinfx-trading-bot:latest "$@"' >> /usr/local/bin/fxcbot && \
    chmod +x /usr/local/bin/fxcbot

# ✅ Ensure xhost commands persist for GUI visibility
RUN echo "xhost +local:docker" >> /etc/bash.bashrc

# ✅ Create an entrypoint script that ensures a working display
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'set -e' >> /entrypoint.sh && \
    echo 'if [ -z "$DISPLAY" ]; then' >> /entrypoint.sh && \
    echo '  export DISPLAY=:0' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo 'echo "Checking for existing X server on $DISPLAY..."' >> /entrypoint.sh && \
    echo 'if ! xset q >/dev/null 2>&1; then' >> /entrypoint.sh && \
    echo '  echo "No X server detected on $DISPLAY, starting Xvfb..."' >> /entrypoint.sh && \
    echo '  Xvfb "$DISPLAY" -screen 0 1024x768x16 &' >> /entrypoint.sh && \
    echo '  timeout=10' >> /entrypoint.sh && \
    echo '  while [ $timeout -gt 0 ]; do' >> /entrypoint.sh && \
    echo '    if xset q >/dev/null 2>&1; then' >> /entrypoint.sh && \
    echo '      break' >> /entrypoint.sh && \
    echo '    fi' >> /entrypoint.sh && \
    echo '    sleep 1' >> /entrypoint.sh && \
    echo '    timeout=$((timeout-1))' >> /entrypoint.sh && \
    echo '  done' >> /entrypoint.sh && \
    echo '  if [ $timeout -eq 0 ]; then' >> /entrypoint.sh && \
    echo '    echo "Failed to start Xvfb. Exiting."' >> /entrypoint.sh && \
    echo '    exit 1' >> /entrypoint.sh && \
    echo '  fi' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    echo 'echo "Allowing X11 connections..."' >> /entrypoint.sh && \
    echo 'xhost +local:docker' >> /entrypoint.sh && \
    echo 'exec /startup.sh' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# ✅ Switch to non-root user for security
USER dockeruser

# ✅ Expose port 5000 for services
EXPOSE 5000

# ✅ Use the entrypoint script to ensure a working display and launch the application
ENTRYPOINT ["/entrypoint.sh"]