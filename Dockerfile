# ✅ Use a lightweight, optimized Python 3.10 base image
FROM python:3.10-slim

# ✅ Set environment variables for non-buffered output & correct timezone
ENV PYTHONUNBUFFERED=1 TZ=UTC DISPLAY=:0

# ✅ Set working directory
WORKDIR /app

# ✅ Copy project files into the container
COPY . .

# ✅ Install required system dependencies (GUI, SSL, WebSockets, Git, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-venv python3-tk libxcb1 tk-dev libxt6 libxrender1 libx11-6 \
    libxss1 libgl1-mesa-glx libglib2.0-0 x11-apps xauth \
    git curl unzip libssl-dev libffi-dev libsqlite3-dev \
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

# ✅ Allow X server access for GUI
RUN echo "xhost +local:docker" >> /etc/bash.bashrc

# ✅ Create a non-root user for better security
RUN useradd -m dockeruser && chown -R dockeruser /app

# ✅ Step 1: Create the fxcbot script in the system-wide path BEFORE switching users
RUN echo '#!/bin/bash' > /usr/local/bin/fxcbot && \
    echo 'docker run --rm -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name coinfx-trading-bot coinfx-trading-bot "$@"' >> /usr/local/bin/fxcbot && \
    chmod +x /usr/local/bin/fxcbot

# ✅ Switch to non-root user
USER dockeruser

# ✅ Expose port 5000 for Flask, FastAPI, or WebSocket services
EXPOSE 5000

# ✅ Define the default command to run the bot inside the virtual environment
CMD ["python", "main.py"]