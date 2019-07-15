import multiprocessing

# general settings
bind = '127.0.0.1:8000'
backlog = 2048
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# log levels
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
