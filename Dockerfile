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
    xvfb && rm -rf /var/lib/apt/lists/*

# ✅ Create /tmp/.X11-unix directory with proper permissions (for Xvfb)
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# ✅ Copy project files
COPY . .

# ✅ Create & verify venv, then install all dependencies in one layer
RUN python3 -m venv /app/venv \
    && /app/venv/bin/python -m ensurepip --default-pip \
    && /app/venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && /app/venv/bin/python -m pip install --no-cache-dir \
       numpy scipy tensorflow-cpu keras pandas \
       scikit-learn websocket-client websockets grpcio protobuf python-dotenv requests \
       ccxt pyjwt cryptography matplotlib ipywidgets flask fastapi uvicorn \
       oandapyV20 \
    && /app/venv/bin/python -m pip uninstall -y six \
    && /app/venv/bin/python -m pip install --no-cache-dir "six>=1.12.0" \
    && /app/venv/bin/python -m pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git \
    && rm -rf /app/.cache /root/.cache /tmp/pip* /var/lib/apt/lists/*

# ✅ Set correct permissions for execution
RUN chmod +x /app/main.py

# ✅ Create a non-root user for security & set permissions
RUN useradd -m dockeruser && chown -R dockeruser /app /app/venv

# ✅ Create startup script for launching the application with Xvfb
RUN echo '#!/bin/bash' > /startup.sh && \
    echo 'echo "🔥 Starting virtual display..."' >> /startup.sh && \
    echo 'Xvfb :0 -screen 0 1024x768x16 &' >> /startup.sh && \
    echo 'export DISPLAY=:0' >> /startup.sh && \
    echo 'echo "🚀 Launching application..."' >> /startup.sh && \
    echo 'exec /app/venv/bin/python /app/main.py' >> /startup.sh && \
    chmod +x /startup.sh

# ✅ Create global fxcbot script BEFORE switching users
RUN echo '#!/bin/bash' > /usr/local/bin/fxcbot && \
    echo 'docker run --rm -it --name coinfx-trading-bot -e DISPLAY=:0 coinfx-trading-bot:latest "$@"' >> /usr/local/bin/fxcbot && \
    chmod +x /usr/local/bin/fxcbot

# ✅ Create an entrypoint script to support command overrides (for sanity checks)
RUN echo '#!/bin/bash' > /entrypoint.sh && \
    echo 'if [ "$#" -gt 0 ]; then' >> /entrypoint.sh && \
    echo '  exec "$@"' >> /entrypoint.sh && \
    echo 'else' >> /entrypoint.sh && \
    echo '  exec /startup.sh' >> /entrypoint.sh && \
    echo 'fi' >> /entrypoint.sh && \
    chmod +x /entrypoint.sh

# ✅ Switch to non-root user for security
USER dockeruser

# ✅ Expose port 5000 for services
EXPOSE 5000

# ✅ Use the entrypoint script to handle headless environments and allow override
ENTRYPOINT ["/entrypoint.sh"]