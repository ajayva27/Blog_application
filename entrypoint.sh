#!/bin/sh

# Wait for the database to be ready
while ! nc -z db 3306; do
    echo "Waiting for MySQL..."
    sleep 1
done

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the Django server
echo "Starting the Django server..."
exec "$@"
