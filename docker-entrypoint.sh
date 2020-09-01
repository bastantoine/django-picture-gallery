#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# From https://stackoverflow.com/questions/33992867/how-do-you-perform-django-database-migrations-when-using-docker-compose

# Apply database migrations
echo "Collect database migrations"
python manage.py makemigrations

# Apply database migrations for the viewer
echo "Apply database migrations for the viewer"
python manage.py makemigrations viewer

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Create default superuser account
echo "Creating default superuser accounts"
python manage.py initadmin

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8080
