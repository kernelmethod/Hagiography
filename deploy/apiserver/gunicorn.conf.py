# Gunicorn configuration file

import os
from multiprocessing import cpu_count

bind = "0.0.0.0:8000"
workers = 2 * cpu_count() + 3
reload = bool(int(os.getenv("GUNICORN_RELOAD", 0)))

if reload:
    print("Running server with --reload enabled")
else:
    print("Running server witout --reload enabled")

# Logging configuration
accesslog = "-"
errorlog = "-"
