import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from uuid import UUID

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

from logic.controller import blue_print as controller_blue_print

######################################
# VARS
######################################

LOG_PATH = os.environ.get(
    'LOG_PATH', f'{Path.home()}/.sensorial/logs/')
LOG_MAX_KB = os.environ.get('LOG_MAX_KB', 1000)
LOG_BACKUP_COUNT = os.environ.get('LOG_BACKUP_COUNT', 2)
LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)

FLASK_PORT = os.environ.get('FLASK_PORT', 5000)
FLASK_HOST = os.environ.get('FLASK_HOST', 'localhost')

SQLITE_PATH = os.environ.get(
    'SQLITE_PATH', f'{Path.home()}/.sensorial/db/sqlite.db')

SEND_BACKEND_MINUTES = os.environ.get('SEND_BACKEND_MINUTES', 2)
SEND_BACKEND_MAX_METRICS = os.environ.get('SEND_BACKEND_MAX_METRICS', 100)
SEND_BACKEND_TRIES = os.environ.get('SEND_BACKEND_TRIES', 3)


######################################
# CODE
######################################

_LOGGER: logging.Logger = None
_APP = None


def config_flask_app(app):

    global _APP
    _APP = app

    error_handler_bp = Blueprint('handlers', __name__)

    @error_handler_bp.app_errorhandler(HTTPException)
    def handle_exception(httpe):
        return '', httpe.code

    @error_handler_bp.app_errorhandler(Exception)
    def handle_exception(e: Exception):
        logger().exception(e)
        return jsonify(e.args), 500

    _APP.register_blueprint(error_handler_bp)
    _APP.register_blueprint(controller_blue_print)


def logger() -> logging.Logger:

    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, exist_ok=True)

    global _LOGGER

    if _LOGGER:
        return _LOGGER

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    rotating = RotatingFileHandler(
        f'{LOG_PATH}/app.log', maxBytes=LOG_MAX_KB * 1000, backupCount=LOG_BACKUP_COUNT)
    rotating.setLevel(LOG_LEVEL)
    rotating.setFormatter(formatter)

    sh = logging.StreamHandler()
    sh.setLevel(LOG_LEVEL)
    sh.setFormatter(formatter)

    _LOGGER = logging.getLogger("app")
    _LOGGER.setLevel(LOG_LEVEL)
    _LOGGER.addHandler(rotating)
    _LOGGER.addHandler(sh)

    return _LOGGER


def get_raspberry_uuid() -> UUID:
    return UUID('a367742e-4121-4365-ad10-863ce98ad4e3')
