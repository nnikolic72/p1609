web: gunicorn squaresensor.wsgi --timeout=120 --log-file -
worker: celery -A squaresensor worker -l info