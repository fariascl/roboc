FROM python:3.13-slim

WORKDIR /app

# Install dependencies required by discord.py voice, yt-dlp, and sqlite
RUN apt-get update && apt-get install -y \
    sqlite3 \
    ffmpeg \
    libsodium-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create storage directory for logs
RUN mkdir -p storage/logs

COPY src/ src/
COPY schema.sql .

# Command to run the bot. If roboc.db doesn't exist, we can initialize it with schema.sql
CMD ["sh", "-c", "if [ ! -f roboc.db ]; then sqlite3 roboc.db < schema.sql; fi && python src/roboc.py"]
