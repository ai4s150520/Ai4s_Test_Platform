# Dockerfile (For Local Development)

# Use an official, slim Python image.
FROM python:3.11-slim

# Set environment variables for better Python performance in Docker.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container.
WORKDIR /app

# Install system-level dependencies.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       libpq-dev \
       netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies.
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and make it executable.
COPY ./entrypoint.sh /app/
# Fix potential Windows line ending issues and make executable
RUN sed -i 's/\r$//g' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set the startup script as the entrypoint for the container.
ENTRYPOINT ["/app/entrypoint.sh"]