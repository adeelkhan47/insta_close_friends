#!/bin/sh

set -e
cd /app/
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install --upgrade undetected-chromedriver
python3 -m pip install webdriver-manager



cd src

while ! alembic upgrade head
do
     echo "Retry..."
     sleep 1
done
#exec celery -A tasks.email worker -l INFO --pool=solo &
#exec celery -A tasks.email beat -l INFO &
exec gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 10000 --forwarded-allow-ips='*' wsgi:app
