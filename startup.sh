#!/bin/sh
set -e
mkdir -p /home/site/data
python manage.py migrate --noinput
exec gunicorn --bind 0.0.0.0:8000 --timeout 120 website.wsgi:application
