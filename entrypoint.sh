#!/bin/sh
# This script ensures the database is available before the Django app starts.

# Exit immediately if a command fails.
set -e

# Define the database host and port. These come from docker-compose.
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for PostgreSQL database at $DB_HOST:$DB_PORT..."

# Use netcat (nc) to poll the database port until it's available.
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up and running."

# Run Django management commands
echo "Applying database migrations..."
python manage.py migrate --noinput

# Execute the main command passed to the script (e.g., the gunicorn command from docker-compose)
exec "$@"