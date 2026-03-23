FROM python:3.13-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    sqlite3 \
    ffmpeg \
    libsodium-dev \
    gcc \
    python3-dev \
    libffi-dev \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY schema.sql .

CMD ["sh", "-c", "if [ ! -f roboc.db ]; then sqlite3 roboc.db < schema.sql; fi && python src/roboc.py"]
