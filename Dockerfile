FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential libopenblas-dev liblapack-dev libx11-6 git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip \
    numpy scipy tensorflow keras pandas scikit-learn websocket-client grpcio protobuf python-dotenv requests \
    && (pip install --no-cache-dir cbpro || pip install --no-cache-dir git+https://github.com/danpaquin/coinbasepro-python.git)

EXPOSE 5000

CMD ["python", "main.py"]
