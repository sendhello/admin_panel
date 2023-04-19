#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear
python manage.py compilemessages -l en -l ru
python manage.py createsuperuser --no-input || true

gunicorn config.wsgi:application --bind 0.0.0.0:8000
