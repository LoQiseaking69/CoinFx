FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-6 \
    python3-tk \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Corrected Python dependencies installation with compatible pinned versions
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        numpy==1.23.5 \
        scipy \
        tensorflow==2.13.0 \
        keras==2.13.1 \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
