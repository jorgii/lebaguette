#!/bin/bash
echo "------------ Wait 5 seconds for db ------------"
sleep 5
echo "------------ Begin DB Migration ------------"
python manage.py migrate
echo "------------ End DB Migration ------------"
echo "------------ Begin Collect Static ------------"
python manage.py collectstatic --noinput
echo "------------ End Collect Static ------------"
echo "------------ Load fixtures ------------"
python manage.py loaddata home/fixtures/users_data.json
echo "------------ Start Web ------------"
python manage.py runserver 0.0.0.0:8000
