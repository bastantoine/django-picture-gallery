#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Start server
echo "Starting server"
gunicorn picture_gallery.wsgi:application --bind 0.0.0.0:8000
