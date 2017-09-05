#!/bin/bash
echo ------------ Begin DB Migration ------------
sleep 5
python manage.py migrate                  # Apply database migrations
echo ------------ End DB Migration ------------
echo ------------ Begin Collect Static ------------
python manage.py collectstatic --noinput  # Collect static files
echo ------------ End Collect Static ------------
# Start dev web server processes!
echo ------------ Start UWSGI ------------
exec python manage.py runserver 0.0.0.0:8000
