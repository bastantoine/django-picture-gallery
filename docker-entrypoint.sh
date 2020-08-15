#!/bin/bash

# From https://stackoverflow.com/questions/33992867/how-do-you-perform-django-database-migrations-when-using-docker-compose

# Apply database migrations
echo "Collect database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8080
