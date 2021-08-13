import logging
import os
from pathlib import Path

VERSION = os.environ.get('VERSION', 'LOCAL')

LOG_DIR = os.environ.get('LOG_DIR', f'{Path.home()}/.sensorial/logs/')
LOG_MAX_KB = int(os.environ.get('LOG_MAX_KB', 1000))
LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 2))
LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)

FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))
FLASK_HOST = os.environ.get('FLASK_HOST', 'localhost')

SQLITE_PATH = os.environ.get(
    'SQLITE_PATH', f'{Path.home()}/.sensorial/db/sqlite.db')

SEND_BACKEND_SECONDS = int(os.environ.get('SEND_BACKEND_SECONDS', 2))
SEND_BACKEND_MAX_METRICS = int(os.environ.get('SEND_BACKEND_MAX_METRICS', 100))
SEND_BACKEND_TRIES = int(os.environ.get('SEND_BACKEND_TRIES', 3))
