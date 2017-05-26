#!/bin/bash
python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files

# Prepare log files and start outputting logs to stdout
touch /lebaguette/logs/gunicorn.log
touch /lebaguette/logs/access.log
tail -n 0 -f /code/logs/*.log &

# Start uwsgi processes
echo Starting uwsgi.
exec uwsgi --ini uwsgi.ini
