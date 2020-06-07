import multiprocessing
import os
from distutils.util import strtobool

SUGGESTED = multiprocessing.cpu_count() * 2 + 1

bind = "0.0.0.0:{0}".format(os.getenv("APP_PORT", "8000"))
workers = int(os.getenv("APP_WORKERS", SUGGESTED))
threads = int(os.getenv("APP_TREADS", SUGGESTED))
reload = bool(strtobool(os.getenv("APP_RELOAD", "false")))
timeout = 30
worker_connections = 1000

# capture_output = True
