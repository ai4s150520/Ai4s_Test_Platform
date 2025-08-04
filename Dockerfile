# Dockerfile

# Start with an official Python image. 'slim' is a smaller version.
FROM python:3.11-slim

# Set environment variables to improve Python's performance in Docker.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the working directory inside the container.
WORKDIR /app

# Install system-level dependencies.
# 'libpq-dev' is needed for the PostgreSQL client.
# 'netcat-openbsd' is a useful tool for checking if the database is ready.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       libpq-dev \
       netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy your requirements.txt file into the container.
# We do this in a separate step to take advantage of Docker's caching.
# Dependencies are only re-installed if this file changes.
COPY ./requirements.txt /app/

# Install the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your entire Django project code into the container's working directory.
COPY . /app/

# The port the container will listen on. This is for Gunicorn.
EXPOSE 8000

# Add and give executable permissions to our startup script.
COPY ./entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Set the startup script as the entrypoint for the container.
ENTRYPOINT ["/app/entrypoint.sh"]