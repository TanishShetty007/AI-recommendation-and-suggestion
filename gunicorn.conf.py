# gunicorn.conf.py - Gunicorn configuration for production
import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# Worker processes
# Formula: (2 × CPU cores) + 1. Good for I/O-bound Flask apps.
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"

# Timeouts – generous to allow Gemini API + database calls
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 120))
keepalive = 5
graceful_timeout = 30

# Logging – stdout/stderr captured by CloudWatch Logs on AWS
accesslog = "-"
errorlog  = "-"
loglevel  = os.environ.get('LOG_LEVEL', 'info')

# Security: limit request line and headers
limit_request_line   = 4096
limit_request_fields = 100

# Prevent memory leaks – recycle each worker after 1000 requests
max_requests          = 1000
max_requests_jitter   = 50
