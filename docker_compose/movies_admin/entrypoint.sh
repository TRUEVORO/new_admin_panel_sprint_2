#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.1
done
echo "PostgreSQL started"

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --config gunicorn/gunicorn.py

exec "$@"
