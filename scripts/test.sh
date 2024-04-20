#!/bin/sh

echo "Running tests on the server..."
python manage.py makemigrations
python manage.py migrate
python manage.py test