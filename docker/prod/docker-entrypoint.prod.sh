#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

LOGFOLDER="$HOME/log"
mkdir -p $LOGFOLDER
touch "$LOGFOLDER/$ACCESS_LOG"
touch "$LOGFOLDER/$ERROR_LOG"

# Start server
echo "Starting server"
gunicorn picture_gallery.wsgi:application --bind 0.0.0.0:8000 --access-logfile "$LOGFOLDER/$ACCESS_LOG" --error-logfile "$LOGFOLDER/$ERROR_LOG"
