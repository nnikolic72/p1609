web: gunicorn squaresensor.wsgi --timeout=30 --log-file -
worker: celery -A squaresensor worker -l info