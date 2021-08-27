import logging
import os
from enum import Enum
from pathlib import Path
from typing import Dict

_defaults = {
    'VERSION': 'LOCAL',
    'LOG_DIR': f'{Path.home()}/.sensorial/logs/',
    'LOG_MAX_KB': '1000',
    'LOG_BACKUP_COUNT': '2',
    'LOG_LEVEL': 'INFO',
    'PORT': '5000',
    'HOST': 'localhost',
    'SQLITE_PATH': f'{Path.home()}/.sensorial/db/sqlite.db',
    'SEND_BACKEND_SECONDS': '15',
    'SEND_BACKEND_MAX_METRICS': '25',
    'SEND_BACKEND_TRIES': '3',
    'SEND_BACKEND_URL': f'http://localhost:5000/api/v1/mocks/backend/metrics'
}


class Vars(Enum):
    VERSION = 'VERSION'
    LOG_DIR = 'LOG_DIR'
    LOG_MAX_KB = 'LOG_MAX_KB'
    LOG_BACKUP_COUNT = 'LOG_BACKUP_COUNT'
    LOG_LEVEL = 'LOG_LEVEL'
    PORT = 'PORT'
    HOST = 'HOST'
    SQLITE_PATH = 'SQLITE_PATH'
    SEND_BACKEND_SECONDS = 'SEND_BACKEND_SECONDS'
    SEND_BACKEND_MAX_METRICS = 'SEND_BACKEND_MAX_METRICS'
    SEND_BACKEND_TRIES = 'SEND_BACKEND_TRIES'
    SEND_BACKEND_URL = 'SEND_BACKEND_URL'


def get(var_name: Vars) -> str:
    return os.environ.get(var_name.value, _defaults.get(var_name.value))


def set(var_name: Vars, value: str):
    os.environ[var_name.value] = str(value)


def current_vars() -> Dict[str, str]:
    return {
        key.value: get(key)
        for key in Vars
    }
