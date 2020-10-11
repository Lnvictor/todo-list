release: python manage.py migrate --noinput
release: python manage.py collectsttatic --noinput
web: gunicorn todosite.wsgi --log-file -
