# Procfile for Railway deployment
# Decision: Use gunicorn for production WSGI server

release: python src/manage.py migrate && python src/manage.py collectstatic --noinput
web: gunicorn --bind 0.0.0.0:$PORT --chdir src config.wsgi:application