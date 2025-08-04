#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the database host and port. The name 'db' is what we will call
# our PostgreSQL service in the docker-compose.yml file.
DB_HOST="db"
DB_PORT="5432"

echo "Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."

# Use netcat (nc) to poll the database port until it's available.
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1 # wait for 1/10 of a second before check again
done

echo "PostgreSQL started successfully."

# Once the database is ready, apply any pending database migrations.
echo "Applying database migrations..."
python manage.py migrate

# Now, execute the main command for the container. This will be the gunicorn
# command that we pass in our docker-compose.yml file.
exec "$@"