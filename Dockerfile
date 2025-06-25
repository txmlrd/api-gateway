# Gunakan image Python
FROM python:3.10-slim

ENV PYTHONPATH=/app

# Set working directory
WORKDIR /app

RUN pip install redis

# Copy semua file ke dalam container
COPY . /app/

# Install dependency Python
RUN pip install --no-cache-dir -r requirements.txt

# Default command

CMD ["python","app/run.py"]
