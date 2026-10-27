# Procfile - Used by AWS Elastic Beanstalk, Heroku, and similar PaaS platforms
# Gunicorn starts the WSGI app with 3 workers and binds to the dynamic $PORT
web: gunicorn wsgi:application --bind 0.0.0.0:${PORT:-5000} --workers 3 --timeout 120 --access-logfile - --error-logfile -
