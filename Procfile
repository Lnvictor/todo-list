release: python manage.py migrate --noinput
release: python manage.py collectstatic --noinput
web: gunicorn todosite.wsgi --log-file -
