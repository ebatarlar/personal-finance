FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

ENV PORT=8080
ENV HOST=0.0.0.0

# Run with reload disabled and increased timeout
CMD uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1 --timeout-keep-alive 75 --log-level debug --no-access-log
