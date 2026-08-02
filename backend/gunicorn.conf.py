"""Gunicorn configuration"""

import multiprocessing

bind = "0.0.0.0:5000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
threads = 2
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
ca_certs = None

# Server hooks
def on_starting(server):
    pass

def when_ready(server):
    pass

def on_exit(server):
    pass
