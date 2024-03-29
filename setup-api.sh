#!/bin/bash

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input --clear

# Set permissions for the static files directory
chmod -R 755 /api/app/static

# Start the Django development server
python manage.py runserver 0.0.0.0:$1 --noreload