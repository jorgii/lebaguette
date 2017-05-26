#!/bin/bash
echo ------------ Begin DB Migration ------------
python manage.py migrate                  # Apply database migrations
echo ------------ End DB Migration ------------
echo ------------ Begin Collect Static ------------
python manage.py collectstatic --noinput  # Collect static files
echo ------------ End Collect Static ------------
echo ------------ Start UWSGI ------------
exec uwsgi --ini uwsgi.ini  # Start uwsgi processes
