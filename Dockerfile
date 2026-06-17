FROM python:3.12-slim

WORKDIR /app

# Install dependencies before copying code to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

ENTRYPOINT ["python", "-m", "src.cli"]