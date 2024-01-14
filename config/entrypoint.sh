#!/bin/bash

APP_PORT=${PORT:-8000}

cd /app/

/opt/venv/bin/python manage.py collectstatic

/opt/venv/bin/python manage.py makemigrations

/opt/venv/bin/python manage.py migrate

# Create admin user
#/opt/venv/bin/python manage.py create_admin_user

# Load fixtures
#/opt/venv/bin/python manage.py loaddata products/fixtures/*

/opt/venv/bin/gunicorn microEcommerce.wsgi:application --bind "0.0.0.0:${APP_PORT}"